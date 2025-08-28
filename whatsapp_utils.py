import logging
from typing import Optional

import httpx

from config import API_VERSION, WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_ID
from get_data import fetch_questions


# --------------------- Utility: HTTP Post Wrapper -----------------------
async def post_to_whatsapp(payload: dict) -> Optional[dict]:
    url = f"https://graph.facebook.com/{API_VERSION}/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Success: {response.status_code} - {response.text}")
            return response.json()
        except httpx.HTTPError as e:
            logging.error(f"WhatsApp API error: {e}")
            return None


# -------------- Send plain text message ---------------------
async def send_message(to_number: str, message: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    await post_to_whatsapp(payload)


# -------- Mark message as read + simulate typing -------------
async def mark_as_read_send_indicator(message_id: str):
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
        "typing_indicator": {
            "type": "text"
        }
    }
    await post_to_whatsapp(payload)


# ---------------- Send a List Message ---------------------
async def send_list(to_number: str):
    rows = await fetch_questions()

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "University Helpdesk"
            },
            "body": {
                "text": "Please choose a topic for your query."
            },
            "action": {
                "button": "Select an Option",
                "sections": [{
                    "title": "Available Topics",
                    "rows": rows
                }]
            }
        }
    }
    await post_to_whatsapp(payload)


# ---------------- Send Yes/No Buttons ---------------------
async def send_yes_no_buttons(to: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Do you want to proceed?"
            },
            "action": {
                "buttons": [{
                    "type": "reply",
                    "reply": {
                        "id": "yes",
                        "title": "Yes"
                    }
                }, {
                    "type": "reply",
                    "reply": {
                        "id": "no",
                        "title": "No"
                    }
                }]
            }
        }
    }
    await post_to_whatsapp(payload)

# ---------------- Send a Template Message ---------------------
import json
from typing import Optional, List, Dict, Any

async def send_template(
    to_number: str,
    template_name: str,
    language: str = "en",
    components: Optional[List[Dict[str, Any]]] = None
):
    
    # payload = {
    #     "messaging_product": "whatsapp",
    #     "to": to_number,
    #     "type": "template",
    #     "template": {
    #         "name": template_name,
    #         "language": {"code": language}
    #     }
    # }

    # # Validate components
    # if components:
    #     if not isinstance(components, list):
    #         raise ValueError("`components` must be a list of dicts")

    #     for comp in components:
    #         if "type" not in comp:
    #             raise ValueError(f"Invalid component: {comp}. Missing 'type'")
    #         if comp["type"] == "body" and "parameters" not in comp:
    #             raise ValueError(f"Body component must include 'parameters': {comp}")

    #     payload["template"]["components"] = components

    payload = {
        "messaging_product": "whatsapp",
        "to": "916378533897",
        "type": "template",
        "template": {
            "name": "otp",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "123456"
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "123456"
                        }
                    ]
                }
            ]
        }
    }

    return await post_to_whatsapp(payload)
