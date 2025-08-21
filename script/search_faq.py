import os
import json
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# === Cosine similarity function ===
def cosine_similarity(vec1, vec2):
    v1, v2 = np.array(vec1), np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
faq_embeddings_path = os.path.join(DATA_DIR, "faq_embeddings.json")

# === Load API key ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# === Load FAQ with embeddings ===
try:
    with open(faq_embeddings_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"❌ Could not find {faq_embeddings_path}")

# === Search loop ===
while True:
    query = input("\n💬 Ask a question (or type 'exit'): ").strip()
    if query.lower() in ["exit", "quit", "q"]:
        break

    # Get embedding for user query
    query_embedding = genai.embed_content(
        model="models/embedding-001",
        content=query
    )["embedding"]

    # Compare with stored embeddings
    scores = [
        (cosine_similarity(query_embedding, item["embedding"]), item)
        for item in faq_data
    ]

    # Sort by highest similarity
    scores.sort(key=lambda x: x[0], reverse=True)

    best_score, best_match = scores[0]
    print(f"\n🔹 Best match (score: {best_score*100:.2f}%):")
    print(f"Q: {best_match['question']}")
    print(f"A: {best_match['answer']}")
