import os
import json
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# === Cosine similarity function ===
def cosine_similarity(vec1, vec2):
    """Calculates the cosine similarity between two vectors."""
    v1, v2 = np.array(vec1), np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# === Configuration and data loading ===
# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI API with the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# Define the paths for the FAQ data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
faq_embeddings_path = os.path.join(DATA_DIR, "faq_embeddings.json")

# Load FAQ data with embeddings
try:
    with open(faq_embeddings_path, "r", encoding="utf-8") as f:
        FAQ_DATA = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"❌ Could not find {faq_embeddings_path}. Please generate it first.")

async def search_faq(user_query: str) -> str:
    """
    Finds the best matching FAQ answer for a user query using embedding similarity.
    
    Args:
        user_query: The user's text message.
        
    Returns:
        The best matching FAQ answer as a string.
    """
    try:
        # Get embedding for user query
        query_embedding = genai.embed_content(
            model="models/embedding-001",
            content=user_query
        )["embedding"]

        # Compare with stored embeddings
        scores = [
            (cosine_similarity(query_embedding, item["embedding"]), item)
            for item in FAQ_DATA
        ]

        # Sort by highest similarity
        scores.sort(key=lambda x: x[0], reverse=True)

        best_score, best_match = scores[0]

        # Define a similarity threshold to avoid returning irrelevant answers
        # A threshold of 0.75 is a good starting point. You can adjust this.
        if best_score > 0.75:
            return best_match['answer']
        else:
            return "I'm sorry, I couldn't find an answer to your question. Please rephrase or try a different question."

    except Exception as e:
        print(f"Error during FAQ search: {e}")
        return "An error occurred while processing your request. Please try again later."
