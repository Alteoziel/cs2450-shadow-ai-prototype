import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

_DB = Path(__file__).resolve().parents[2] / "data" / "shadow.db"


def _connect():
    _DB.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(_DB)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS confirmations (
          id TEXT PRIMARY KEY,
          prompt_text TEXT NOT NULL,
          text_sent TEXT,
          secret_count INTEGER NOT NULL,
          flagged TEXT NOT NULL,
          choice TEXT NOT NULL,
          model TEXT,
          reply TEXT,
          created_at TEXT NOT NULL
        )
        """
    )
    return connection


class PromptStore:
    def save_held(self, prompt_id, prompt_text, secret_count, flagged, model) -> None:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with _connect() as connection:
            connection.execute(
                """
                INSERT INTO confirmations
                  (id, prompt_text, text_sent, secret_count, flagged, choice, model, reply, created_at)
                VALUES (?, ?, '', ?, ?, 'held', ?, '', ?)
                ON CONFLICT(id) DO UPDATE SET
                  prompt_text = excluded.prompt_text,
                  secret_count = excluded.secret_count,
                  flagged = excluded.flagged,
                  model = excluded.model
                """,
                (prompt_id, prompt_text, secret_count, json.dumps(flagged), model, now),
            )

    def save_confirmation(
        self, prompt_id, prompt_text, text_sent, secret_count, choice, model, reply="", flagged=None
    ) -> None:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        flagged_json = json.dumps(flagged or [])
        with _connect() as connection:
            connection.execute(
                """
                INSERT INTO confirmations
                  (id, prompt_text, text_sent, secret_count, flagged, choice, model, reply, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                  text_sent = excluded.text_sent,
                  secret_count = excluded.secret_count,
                  choice = excluded.choice,
                  model = excluded.model,
                  reply = excluded.reply
                """,
                (
                    prompt_id,
                    prompt_text,
                    text_sent,
                    secret_count,
                    flagged_json,
                    choice,
                    model,
                    reply,
                    now,
                ),
            )

    def flagged_report(self, model: str | None = None, blocked_only: bool = False) -> dict:
        clauses, params = [], []
        if model:
            clauses.append("model = ?")
            params.append(model)
        if blocked_only:
            clauses.append("choice = ?")
            params.append("blocked")
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with _connect() as connection:
            rows = connection.execute(
                f"""
                SELECT id, prompt_text, text_sent, secret_count, flagged, choice, model, reply, created_at
                FROM confirmations
                {where}
                ORDER BY created_at DESC
                """,
                params,
            ).fetchall()
        return {
            "status": "ok",
            "rows": [
                {
                    "id": row["id"],
                    "prompt_text": row["prompt_text"],
                    "text_sent": row["text_sent"],
                    "secret_count": row["secret_count"],
                    "flagged": json.loads(row["flagged"] or "[]"),
                    "choice": row["choice"],
                    "model": row["model"],
                    "reply": row["reply"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ],
        }
