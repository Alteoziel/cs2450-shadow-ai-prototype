# Shadow-AI Gateway

Employee chat for the Submit Prompt use case. The app flags sensitive text, asks the employee to confirm, then sends either a redacted prompt or the original prompt to a mock AI provider.

## Run

```powershell
cd Shadow-AI-Gateway
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --port 8000
```

Open http://127.0.0.1:8000

Click **Use sample prompt**, then **Submit prompt**. Choose **Apply redaction** or **Keep original**.

No API key is required. The model list is Mock OpenAI and Mock Anthropic.
