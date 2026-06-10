import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest_documents

COLLECTION_NAME = "pesticide_labels"
EMBED_MODEL = "all-MiniLM-L6-v2"


def build_vector_store(documents_dir="documents"):
    """Embed all chunks and store in ChromaDB."""

    # Load and chunk documents
    print("Loading and chunking documents...")
    chunks = ingest_documents(documents_dir)

    if not chunks:
        print("No chunks to embed. Exiting.")
        return

    # Load embedding model
    print(f"\nLoading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    # Set up ChromaDB
    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")

    # Delete existing collection if it exists (fresh rebuild)
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    # Embed and store in batches
    print(f"\nEmbedding {len(chunks)} chunks...")
    batch_size = 100

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            ids=[f"{c['source']}_{c['chunk_index']}" for c in batch],
            embeddings=embeddings,
            documents=texts,
            metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in batch]
        )
        print(f"  Embedded chunks {i+1}–{min(i+batch_size, len(chunks))}")

    print(f"\nDone! {collection.count()} chunks stored in ChromaDB.")
    return collection


def retrieve(query, top_k=5):
    """Retrieve top-k relevant chunks for a query."""
    model = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 4)
        })

    return chunks


if __name__ == "__main__":
    # Build the vector store
    build_vector_store()

    # Test retrieval with 3 evaluation questions
    test_queries = [
        "What is the mixing rate for Monterey Garden Insect Spray?",
        "What is the preharvest interval for BotaniGard 22WP?",
        "Can ZeroTol HC be tank mixed with copper fungicides?",
    ]

    print("\n--- RETRIEVAL TEST ---\n")
    for query in test_queries:
        print(f"Query: {query}")
        results = retrieve(query)
        for r in results:
            print(f"  [{r['distance']}] ({r['source']}) {r['text'][:120]}...")
        print()