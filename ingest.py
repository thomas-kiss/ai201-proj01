import os
import pdfplumber

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_pdf(filepath):
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def clean_text(text):
    """Clean extracted PDF text."""
    import re
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove lines that are just page numbers or dashes
    text = re.sub(r'^\s*[\d\-]+\s*$', '', text, flags=re.MULTILINE)
    # Collapse multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks with source metadata."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_index": len(chunks)
            })
        start += chunk_size - overlap
    return chunks


def ingest_documents(documents_dir=DOCUMENTS_DIR):
    """Load, clean, and chunk all PDFs in the documents directory."""
    all_chunks = []

    pdf_files = [f for f in os.listdir(documents_dir) if f.endswith(".pdf")]

    if not pdf_files:
        print(f"No PDF files found in {documents_dir}")
        return all_chunks

    for filename in sorted(pdf_files):
        filepath = os.path.join(documents_dir, filename)
        print(f"Processing {filename}...")

        raw_text = load_pdf(filepath)
        if not raw_text.strip():
            print(f"  WARNING: No text extracted from {filename} — may be a scanned PDF")
            continue

        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned, source=filename)
        all_chunks.extend(chunks)
        print(f"  -> {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = ingest_documents()

    print("\n--- 5 SAMPLE CHUNKS ---\n")
    import random
    samples = random.sample(chunks, min(5, len(chunks)))
    for i, chunk in enumerate(samples):
        print(f"[Chunk {i+1}] Source: {chunk['source']} | Index: {chunk['chunk_index']}")
        print(chunk['text'])
        print("-" * 60)