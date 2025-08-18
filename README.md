# WhatsApp Cloud API Chatbot 🚀

A WhatsApp Cloud API chatbot built using **FastAPI**.

- Handles incoming messages via **webhook**  
- Fetches **questions, sub-questions, and answers** from external APIs  
- Uses `.env` for secure configuration (tokens, API keys, and URLs)  
- Ready for deployment on **VPS or cloud hosting**

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root folder:

```env
WEBHOOK_VERIFY_TOKEN=your_verify_token
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_ID=your_phone_id
API_VERSION=v23.0

URL_FOR_QUESTIONS=https://whatsapp.solvebee.in/getQuestions.php
URL_FOR_SUB_QUESTIONS=https://whatsapp.solvebee.in/getSubQuestions.php
URL_FOR_ANSWER=https://whatsapp.solvebee.in/getAnswer.php
```

---

## ▶️ Run the App

Start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌍 Deployment

For VPS or cloud hosting:
1. Upload the project to your server.  
2. Set up Python and dependencies.  
3. Add your `.env` file on the server.  
4. Run the app with `uvicorn` or `gunicorn`.  
5. Point your **WhatsApp Cloud API webhook** to:  
   ```
   https://your-domain.com/webhook
   ```

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – Web framework  
- [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api) – Messaging API  
- [Python-Dotenv](https://pypi.org/project/python-dotenv/) – Environment variable loader  

---

## 📄 License
This project is licensed under the MIT License.
