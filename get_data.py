import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# API URLs
URL_FOR_QUESTIONS = os.getenv("URL_FOR_QUESTIONS")
URL_FOR_SUB_QUESTIONS = os.getenv("URL_FOR_SUB_QUESTIONS")
URL_FOR_ANSWER = os.getenv("URL_FOR_ANSWER")

user_sub_questions = {}


# Fetch the question list from API and convert to WhatsApp format
async def fetch_questions():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL_FOR_QUESTIONS)
            response.raise_for_status()
            data = response.json()

        # print("Feched data from API.")

        # Format data for WhatsApp list
        return [{
            "id": str(item["Id"]),
            "title": item["Question"]
        } for item in data.get("Questions", [])]

    except Exception as e:
        print("Error fetching questions:", e)
        return []


# Fetch follow-up questions
async def fetch_followup_questions(question_id: str, user_number: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(URL_FOR_SUB_QUESTIONS,
                                         json={"questionId": question_id})
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        print("Error fetching follow-up questions:", e)
        return "❌ Unable to fetch questions at the moment."

    questions = data.get("Questions", [])
    if not questions:
        return "No questions found for your selection."

    # Save index-to-ID map
    user_sub_questions[user_number] = {
        idx + 1: q["Id"]
        for idx, q in enumerate(questions)
    }

    # Format message for user
    message_text = "📘 Related Questions :\n\n"
    for idx, q in enumerate(questions, start=1):
        message_text += f"{idx}. {q['Question']}\n\n"

    message_text += "💬 Please reply with the number corresponding to your question."

    return message_text.strip()


# Fetch answer based on subQuestionId
async def fetch_answer(sub_question_id: str) -> str:
    payload = {"subQuestionId": sub_question_id}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(URL_FOR_ANSWER, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("Message") == "question found" and "Answer" in data:
                return data["Answer"]
            else:
                return "Sorry, no answer found for this question."
    except Exception as e:
        print(f"Error fetching answer: {e}")
        return "Sorry, something went wrong while getting the answer."
