class PromptStore:
    def save_confirmation(self, prompt_text, text_sent, secret_count, choice, model) -> None:
        """Dillon: persist one confirmed send. Leave this as a no-op until then.

        See docs/DILLON.md for the table and the click-through check.
        """
        return None

    def flagged_report(self) -> dict:
        """Dillon: return the saved rows. The report button already renders this."""
        return {"status": "not yet", "rows": []}
