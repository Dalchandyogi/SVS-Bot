import csv
import requests
import dotenv
import os

dotenv.load_dotenv()


# Your WhatsApp API details
# ACCESS_TOKEN = "EAAiZCirOnCLEBPDYTrwfZCpZBcakkhePeacyS7s3FnBxJ8mYCbNGbezYXian6p5nuhsmsxto0ZBXRUbTeZC8UO9XBZAq7L6BiPgMavkcyNtsYry5TZC7MC8XnBvTys4iWgOoZCjoouZCbbhXsZC8yTfYiZACOMVmdZBKnGfTyWuEQ2Pf1WXZAD47dCvff8Idunk3Cm7uWs0oV6yFS7oI5dKG83qmSFA7PFfVEIOZB338nFycpU3cpCQxcZD"
# PHONE_NUMBER_ID = "782711078253467"
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"


# Read CSV
with open("numbers.csv", "r") as file:
  reader = csv.DictReader(file)
  for row in reader:
    phone_number = row["phone_number"]

    payload = {
      "messaging_product": "whatsapp",
      "to": phone_number,
      "type": "template",
      "template": {
        "name": "hello_world",
        "language": {"code": "en_US"}
      }
    }

    headers = {
      "Authorization": f"Bearer {ACCESS_TOKEN}",
      "Content-Type": "application/json"
   }

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

    print(f"{phone_number} | {response.status_code} | {response.text}\n")
