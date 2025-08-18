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

app = FastAPI()

TEST_NO = os.getenv("TEST_NO")


@app.get("/")
async def index():
    await send_message(TEST_NO, "Hello from Swami Vivekanad Bot!")
    print("Message sent.")
    return {"status": "ok"}


# Webhook verification endpoint
@app.get("/webhook")
async def verify(request: Request):
    params = dict(request.query_params)

    # print("Params:", params)

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
        statuses = entry.get("statuses", [None])[0]
        messages = entry.get("messages", [None])[0]

        if statuses:
            print(f"""
            ===== **** MESSAGE STATUS **** ======
            STATUS  => {statuses.get("status")}
            """)

        if messages:
            user_number = messages["from"]
            msg_type = messages["type"]
            message_id = messages["id"]

            # print(f"MOBILE NUMBER : {user_number}")

            # print(f"Message id : {message_id}")
            await mark_as_read_send_indicator(message_id)

            # Handle Text Input
            if msg_type == "text":
                user_text = messages["text"]["body"].strip().lower()

                # Greeting
                if user_text in ["hi", "hello", "hii"]:
                    await send_message(user_number,
                                       "Welcome! How can I help you today?")
                    await send_list(user_number)

                # User replies with a number (after receiving follow-up question list)
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

            # Handle list reply (user selects a main category)
            elif msg_type == "interactive":
                interactive_obj = messages["interactive"]

                if interactive_obj["type"] == "list_reply":
                    selected_id = interactive_obj["list_reply"]["id"]
                    print(f"Selected ID ====>> : {selected_id}")

                    # Fetch and send follow-up questions
                    msg = await fetch_followup_questions(
                        selected_id, user_number)
                    await send_message(user_number, msg)

                elif interactive_obj["type"] == "button_reply":
                    button_id = interactive_obj["button_reply"]["id"]
                    if button_id == "yes":
                        await send_message(user_number,
                                           "Great! Let's proceed.")
                        await send_list(user_number)
                    else:
                        await send_message(user_number,
                                           "Thank you for your time!")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error:", e)

    return {"status": "ok"}
