# Shadow-AI Gateway

Employee chat for the Submit Prompt use case. The app flags sensitive text, asks the employee to confirm redaction, then sends only the redacted prompt. Every original prompt is stored for the office admin.

## Run

```powershell
cd Shadow-AI-Gateway
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
.\.venv\Scripts\python -m uvicorn app.main:app --port 8000
```

Open http://127.0.0.1:8000

Click **Use sample prompt**, then **Submit prompt**, then **Apply redaction and send**.

Mock OpenAI and Mock Anthropic work with no company key. The demo admin password in `.env` is `cedar-demo`. Open http://127.0.0.1:8000/admin to read the prompt log and to save an OpenAI, Anthropic, or Gemini key. Those keys stay in `data/` on this computer. After a key is saved, that company's models show up in the employee model list. The built-in test key is `shadow-test`. Saving it for a company unlocks that company's models and answers locally, without calling the company.
