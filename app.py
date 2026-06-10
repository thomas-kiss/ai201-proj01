import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv
from embed import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def ask(question):
    """Retrieve relevant chunks and generate a grounded answer."""

    # Retrieve top-5 chunks
    chunks = retrieve(question, top_k=5)

    # Build context string with source labels
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"[Source: {chunk['source']}]\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)

    # Grounded system prompt
    system_prompt = """You are a pesticide label assistant. Your job is to answer questions about pesticide products using ONLY the information provided in the document excerpts below.

Rules:
- Answer ONLY from the provided excerpts. Do not use any outside knowledge.
- Always cite which document(s) your answer comes from, using the source filename.
- If the excerpts do not contain enough information to answer the question, say exactly: "I don't have enough information in the provided labels to answer that."
- Do not guess, infer, or fill in missing information from general knowledge.
- Be concise and specific."""

    user_prompt = f"""Document excerpts:
{context}

Question: {question}

Answer based only on the excerpts above, and cite the source document(s)."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=512
    )

    answer = response.choices[0].message.content

    # Collect unique sources
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {"answer": answer, "sources": sources, "chunks": chunks}


def handle_query(question):
    """Gradio handler."""
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources_text = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources_text


# Build Gradio UI
with gr.Blocks(title="Pesticide Label Assistant") as demo:
    gr.Markdown("# 🌱 Pesticide Label Assistant")
    gr.Markdown("Ask questions about mixing rates, preharvest intervals, application schedules, and product compatibility. Answers are drawn only from the loaded pesticide labels.")

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. What is the mixing rate for Monterey Garden Insect Spray?",
            lines=2
        )

    btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Retrieved from", lines=8)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

    gr.Markdown("### Example questions")
    gr.Examples(
        examples=[
            ["What is the mixing rate for Monterey Garden Insect Spray?"],
            ["What is the preharvest interval for BotaniGard 22WP?"],
            ["What pests does AzaMax control?"],
            ["Can ZeroTol HC be tank mixed with copper fungicides?"],
            ["How often should Arber Bio Protectant be applied for active disease?"],
        ],
        inputs=inp
    )

if __name__ == "__main__":
    demo.launch()