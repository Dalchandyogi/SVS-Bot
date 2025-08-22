import os
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

from config import WEBHOOK_VERIFY_TOKEN
from get_data import fetch_answer, fetch_followup_questions, user_sub_questions
from whatsapp_utils import (
    mark_as_read_send_indicator,
    send_list,
    send_message,
    send_yes_no_buttons,
)
from script.search_faq import search_faq
from script.ask_gemini_faq import ask_faq

app = FastAPI()

load_dotenv()

TEST_NO = os.getenv("TEST_NO")

USE_FAQ_SEARCH = True


@app.get("/")
async def index():
    await send_message(TEST_NO, "Hello from Swami Vivekanad Bot!")
    print("Message sent.")
    return {"status": "ok"}


# Webhook verification endpoint
@app.get("/webhook")
async def verify(request: Request):
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        return PlainTextResponse(status_code=403)


@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    try:
        entry = body["entry"][0]["changes"][0]["value"]
        messages = entry.get("messages", [None])[0]

        if messages:
            user_number = messages["from"]
            msg_type = messages["type"]
            message_id = messages["id"]
            
            await mark_as_read_send_indicator(message_id)

            # Handle Text Input
            if msg_type == "text":
                user_text = messages["text"]["body"].strip().lower()

                # === CONDITIONAL LOGIC BASED ON USE_FAQ_SEARCH ===
                if USE_FAQ_SEARCH:
                    # Search for an answer in the FAQ database
                    faq_answer = await ask_faq(user_text, user_text)
                    await send_message(user_number, faq_answer)

                else:
                    # Use the original interactive menu flow
                    if user_text in ["hi", "hello", "hii"]:
                        await send_message(user_number,
                                           "Welcome! How can I help you today?")
                        await send_list(user_number)

                    elif user_text.isdigit():
                        index = int(user_text)
                        sub_map = user_sub_questions.get(user_number, {})
                        sub_question_id = sub_map.get(index)

                        if sub_question_id:
                            answer = await fetch_answer(str(sub_question_id))
                            await send_message(user_number, answer)
                            await send_yes_no_buttons(user_number)
                        else:
                            await send_message(
                                user_number,
                                "Please select a valid option from the previous Questions list."
                            )

                    else:
                        await send_message(
                            user_number,
                            "Sorry, I didn't understand that. Please type 'hi' or 'hello' to start."
                        )

            # Handle list and button replies for the original flow
            elif msg_type == "interactive":
                interactive_obj = messages["interactive"]
                
                if interactive_obj["type"] == "list_reply":
                    selected_id = interactive_obj["list_reply"]["id"]
                    print(f"Selected ID ====>> : {selected_id}")

                    msg = await fetch_followup_questions(selected_id, user_number)
                    await send_message(user_number, msg)

                elif interactive_obj["type"] == "button_reply":
                    button_id = interactive_obj["button_reply"]["id"]
                    if button_id == "yes":
                        await send_message(user_number, "Great! Let's proceed.")
                        await send_list(user_number)
                    else:
                        await send_message(user_number, "Thank you for your time!")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error:", e)

    return {"status": "ok"}
