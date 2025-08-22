import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from docx import Document

# === Load API Key ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# === Load FAQ document (docx) and extract text ===
def load_faq_docx(doc_path):
    doc = Document(doc_path)
    text_parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(text_parts)

# Path to your FAQ doc
faq_path = "data/FAQ of SVS.docx"
faq_text = load_faq_docx(faq_path)

# === Ask Gemini with FAQ content as context ===
def ask_faq(question, faq_text):
    prompt = f"""
        You are a helpful FAQ assistant. Your task is to answer user questions
        ONLY using the following FAQ content.

        --- FAQ Content Start ---
        {faq_text}
        --- FAQ Content End ---

        Question:
        {question}

        Guidelines for your answer:
        - Always begin your answer with one short introductory sentence before listing details.
        - If multiple points are relevant, list them as clear bullet points (use this •) and separate each point with a newline.
        - Keep answers concise and easy to read.
        - Answer only from the FAQ text, do not invent anything new.
        - If the information is not found in the FAQ, reply: "❌ Not available in FAQ."
    """

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

# === Run ===
if __name__ == "__main__":
    while True:
        q = input("\n💬 Ask a question (or type 'exit'): ").strip()
        if q.lower() in ["exit", "quit"]:
            break

        answer = ask_faq(q, faq_text)
        print(f"\n🤖 Answer: \n{answer}")
