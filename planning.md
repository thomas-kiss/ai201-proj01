# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Pesticide labels for biological/organic garden inputs. Hard to find because labels are dense PDFs scattered across EPA and manufacturer websites. Growers rarely have them when mixing in the field.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | monterey_spinosad.pdf | Monterey Garden Insect Spray (Spinosad) label | https://www.montereylawngarden.com/wp-content/uploads/2018/04/MontereyGardenInsectSpray-2-column-08-0111-Bilingual.pdf |
| 2 | azamax.pdf | AzaMax Azadirachtin insecticide/miticide label | https://www.planetnatural.com/wp-content/uploads/2017/10/azamax-product-label.pdf |
| 3 | azamax_wa.pdf | AzaMax Washington state label (EPA registered) | https://picol.cahnrs.wsu.edu/DownloadLabel/51038/WA/WA_2025_71908-1-81268_AZAMAX.pdf |
| 4 | regalia_gc.pdf | Regalia GC Biofungicide, Marrone Bio Innovations | https://www3.epa.gov/pesticides/chem_search/ppls/084059-00003-20191219.pdf |
| 5 | zerotol_hc.pdf | ZeroTol HC broad-spectrum algaecide/fungicide | https://biosafesystems.com/wp-content/uploads/2020/08/zerotol-hc_label.pdf |
| 6 | botanigard_22wp.pdf | BotaniGard 22WP mycoinsecticide, Certis Bio | https://www.certisbio.com/hubfs/BotaniGard%2022WP_Specimen%20Label.pdf |
| 7 | botanigard_22wp_epa.pdf | BotaniGard 22WP EPA registered label | https://www3.epa.gov/pesticides/chem_search/ppls/082074-00002-20210722.pdf |
| 8 | monterey_bt.pdf | Monterey B.t. (Bacillus thuringiensis) label | https://www.montereylawngarden.com/wp-content/uploads/2024/07/MontereyBt-2-column-Specimen-Label_12-01-22_05.pdf |
| 9 | arber_bio_fungicide.pdf | Arber Bio Fungicide label | https://cdn.commercev3.net/cdn.arbico-organics.com/downloads/1314782_ArberBioInsecticide_label.pdf |
| 10 | arber_bio_protectant.pdf | Arber Bio Protectant (immune booster) label | https://cdn.commercev3.net/cdn.arbico-organics.com/downloads/1314780_ArberBioProtectant_label-booklet.pdf |
| 11 | arber_bio_insecticide.pdf | Arber Bio Insecticide label | https://cdn.commercev3.net/cdn.arbico-organics.com/downloads/1314782_ArberBioInsecticide_label.pdf |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 char

**Overlap:** 100 char

**Reasoning:** Long techincal PDFS

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** Cost, lateny and accuracy for free vs paid API models.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the mixing rate for Monterey Garden Insect Spray? | 2 oz (4 Tbsp) per gallon of water |
| 2 | What is the preharvest interval for BotaniGard 22WP? | 0 days. It can be applied up to and on the day of harvest |
| 3 | What pests does AzaMax control? | Spider mites, thrips, fungus gnats, aphids, whiteflies, leaf miners, worms, beetles, and other listed pests |
| 4 | Can ZeroTol HC be tank mixed with copper-based fungicides? | No. Do not tank mix with copper or other metal-based pesticides |
| 5 | How often should Arber Bio Protectant be applied for active disease control? | Every 7-10 days for active disease, every 10-14 days for general wellness |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Chunk boundry

2. PDF layouts? Some use tables and charts

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

[PDF Documents: 11 label files in /documents]
|
v
[Ingestion: pdfplumber — extract text, clean whitespace and artifacts]
|
v
[Chunking: 500-char chunks, 100-char overlap, source filename attached as metadata]
|
v
[Embedding: sentence-transformers all-MiniLM-L6-v2 — runs locally]
|
v
[Vector Store: ChromaDB — stores embeddings + source metadata, runs locally]
|
v
[Retrieval: semantic similarity search, top-5 chunks returned with source names]
|
v
[Generation: Groq API, llama-3.3-70b-versatile — grounded prompt, context-only answers]
|
v
[Query Interface: Gradio web UI — text input, answer output, sources displayed]

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Give Claude the Documents table (11 PDF files in /documents), the Chunking Strategy section (500 chars, 100 overlap), and the Architecture diagram. Ask it to generate ingest.py (a script that loads each PDF with pdfplumber, cleans the extracted text, splits into chunks using the specified size and overlap, and attaches the source filename as metadata to each chunk) Verify by printing 5 random chunks and checking they are readable, complete thoughts with no HTML artifacts.

**Milestone 4 — Embedding and retrieval:**
Give Claude the Retrieval Approach section and the Architecture diagram. Ask it to generate embed.py (a script that takes the chunks from ingest.py, embeds them with all-MiniLM-L6-v2, and stores them in a local ChromaDB collection with source metadata.) I'll also ask it to generate a retrieve() function that accepts a query string and returns the top-5 chunks with source names. Verify by running 3 of my evaluation questions and checking that returned chunks visibly relate to each question.

**Milestone 5 — Generation and interface:**
Give Claude the Architecture diagram, the grounding requirement (answer only from retrieved context, cite sources), and the Gradio skeleton from the project instructions. Ask it to generate app.py that connects the retrieve() function to the Groq API with a system prompt that enforces grounding, and wraps it in a Gradio UI with a question input, answer output, and sources output. Verify by asking a question my documents don't cover and confirming the system declines rather than hallucinating.

