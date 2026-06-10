# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Pesticide labels for biological and organic garden inputs. This knowledge is valuable because growers need quick answers about mixing rates, application intervals, preharvest intervals, and product compatibility — but the actual labels are dense, multi-page PDFs scattered across EPA and manufacturer websites. When mixing products in the field, nobody has the label open. This system makes that information instantly searchable by plain-language question.


---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | monterey_spinosad.pdf | PDF | https://www.montereylawngarden.com/wp-content/uploads/2018/04/MontereyGardenInsectSpray-2-column-08-0111-Bilingual.pdf |
| 2 | azamax.pdf | PDF | https://www.planetnatural.com/wp-content/uploads/2017/10/azamax-product-label.pdf |
| 3 | azamax_wa.pdf | PDF | https://picol.cahnrs.wsu.edu/DownloadLabel/51038/WA/WA_2025_71908-1-81268_AZAMAX.pdf |
| 4 | regalia_gc.pdf | PDF | https://www3.epa.gov/pesticides/chem_search/ppls/084059-00003-20191219.pdf |
| 5 | zerotol_hc.pdf | PDF | https://biosafesystems.com/wp-content/uploads/2020/08/zerotol-hc_label.pdf |
| 6 | botanigard_22wp.pdf | PDF | https://www.certisbio.com/hubfs/BotaniGard%2022WP_Specimen%20Label.pdf |
| 7 | botanigard_22wp_epa.pdf | PDF | https://www3.epa.gov/pesticides/chem_search/ppls/082074-00002-20210722.pdf |
| 8 | monterey_bt.pdf | PDF | https://www.montereylawngarden.com/wp-content/uploads/2024/07/MontereyBt-2-column-Specimen-Label_12-01-22_05.pdf |
| 9 | arber_bio_fungicide.pdf | PDF | https://cdn.commercev3.net/cdn.arbico-organics.com/downloads/1314782_ArberBioInsecticide_label.pdf |
| 10 | arber_bio_protectant.pdf | PDF | https://cdn.commercev3.net/cdn.arbico-organics.com/downloads/1314780_ArberBioProtectant_label-booklet.pdf |
| 11 | arber_bio_insecticide.pdf | PDF | https://cdn.commercev3.net/cdn.arbico-organics.com/downloads/1314782_ArberBioInsecticide_label.pdf |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 char

**Overlap:** 100 char

**Why these choices fit your documents:** Long technical PDFS

**Final chunk count:** 1142 chunks across 11 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** Cost, lateny and accuracy for free vs paid API models.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

You are a pesticide label assistant. Your job is to answer questions about pesticide
products using ONLY the information provided in the document excerpts below.
Rules:

Answer ONLY from the provided excerpts. Do not use any outside knowledge.
Always cite which document(s) your answer comes from, using the source filename.
If the excerpts do not contain enough information to answer the question, say exactly:
"I don't have enough information in the provided labels to answer that."
Do not guess, infer, or fill in missing information from general knowledge.
Be concise and specific.

**How source attribution is surfaced in the response:**

Each retrieved chunk is labeled with its source filename before being passed to the model as context (e.g. `[Source: monterey_spinosad.pdf]`). The model is instructed to cite these filenames in its answer. Additionally, the Gradio UI displays a separate "Retrieved from" box listing all source filenames programmatically, independent of the model's response.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the mixing rate for Monterey Garden Insect Spray? | 2 oz (4 Tbsp) per gallon of water | Correctly stated 2 fl oz per gallon for hose-end sprayer; noted BT rate was for a different product | Partially relevant — pulled chunks from monterey_bt.pdf and botanigard despite being about a different product | Accurate |
| 2 | What is the preharvest interval for BotaniGard 22WP? | 0 days | Correctly stated 0-day PHI, can be applied up to day of harvest | Relevant — top results from botanigard_22wp.pdf and botanigard_22wp_epa.pdf | Accurate |
| 3 | What pests does AzaMax control? | Spider mites, thrips, fungus gnats, aphids, whiteflies, and more | Returned detailed list by pest order including mites, sawflies, orthoptera, hemiptera | Relevant — all results from azamax.pdf and azamax_wa.pdf | Accurate |
| 4 | Can ZeroTol HC be tank mixed with copper fungicides? | No | Returned "I don't have enough information in the provided labels to answer that." | Off-target — retrieved chunks from zerotol_hc.pdf but none contained the copper compatibility warning | Inaccurate |
| 5 | How often should Arber Bio Protectant be applied for active disease? | Every 7-10 days | Correctly stated 7-day schedule for active disease | Relevant — top result from arber_bio_protectant.pdf | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "Can ZeroTol HC be tank mixed with copper fungicides?"

**What the system returned:** "I don't have enough information in the provided labels to answer that." — even though the ZeroTol HC label does contain a compatibility warning about copper.

**Root cause (tied to a specific pipeline stage):** Chunking/retrieval. maybe no chunck contained copper and prohibited?

**What you would change to fix it:** Increase chunk size or paragaraph level.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
