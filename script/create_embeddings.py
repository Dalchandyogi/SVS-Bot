import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# === Path setup ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

faq_path = os.path.join(DATA_DIR, "faq.json")
faq_embeddings_path = os.path.join(DATA_DIR, "faq_embeddings.json")

# === Load API key ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# === Load your FAQ data ===
try:
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"❌ Could not find faq.json at {faq_path}")

embedded_faq = []

# === Loop through questions and generate embeddings ===
for idx, item in enumerate(faq_data, start=1):
    question = item.get("question", "").strip()
    if not question:
        print(f"⚠️ Skipping empty question at index {idx}")
        continue

    print(f"🔹 Processing {idx}/{len(faq_data)}: {question[:60]}...")

    try:
        embedding = genai.embed_content(
            model="models/embedding-001",  # text embedding model
            content=question
        )["embedding"]
    except Exception as e:
        print(f"❌ Failed to get embedding for: {question[:50]} - {e}")
        continue

    item["embedding"] = embedding
    embedded_faq.append(item)

# === Save to a new file ===
with open(faq_embeddings_path, "w", encoding="utf-8") as f:
    json.dump(embedded_faq, f, ensure_ascii=False, indent=2)

print(f"\n✅ Generated embeddings for {len(embedded_faq)} questions.")
print(f"💾 Saved to: {faq_embeddings_path}")
