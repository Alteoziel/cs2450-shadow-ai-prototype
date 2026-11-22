# Dillon: flagged-data report

The Submit Prompt flow already runs. Your piece is saving each confirmed send and showing it on the Flagged report button. The button, the route, and the call are already wired. You only change `app/database/store.py`.

## What already happens

After the employee confirms (apply redaction or keep original), `Prompt.send` calls:

```python
PromptStore().save_confirmation(
    prompt_text=...,   # the text they typed
    text_sent=...,      # the text that actually went to the model
    secret_count=...,   # how many spans were flagged
    choice=...,         # "apply" or "keep"
    model=...,          # "mock-openai" or "mock-anthropic"
)
```

That method is a no-op right now. `flagged_report()` returns `{"status": "not yet", "rows": []}`. The page already fetches `GET /api/v1/report` and, once `status` is `"ok"`, draws `rows`.

## What to write

Use sqlite at `data/shadow.db` (that folder is gitignored via `data/*.db`). Create the table if it is missing:

```sql
CREATE TABLE IF NOT EXISTS confirmations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  prompt_text TEXT NOT NULL,
  text_sent TEXT NOT NULL,
  secret_count INTEGER NOT NULL,
  choice TEXT NOT NULL,
  model TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

`save_confirmation` inserts one row. `flagged_report` reads every row, newest first, and returns:

```python
{"status": "ok", "rows": [{"id": 1, "prompt_text": "...", "text_sent": "...", "secret_count": 5, "choice": "apply", "model": "mock-openai", "created_at": "..."}]}
```

Keep both method names. The rest of the app calls them by those names.

## Click-through check

1. Follow the README and open http://127.0.0.1:8000
2. Click **Use sample prompt**, then **Submit prompt**, then **Apply redaction**
3. Click **Flagged report**
4. The panel should list that prompt, the placeholder text that was sent, the secret count, and the model

Do this twice, once with **Keep original**, and both rows should show up.
