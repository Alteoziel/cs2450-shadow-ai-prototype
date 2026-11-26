# Dillon

Dillon's piece is the filter on the admin prompt log.

`PromptStore.flagged_report(model, blocked_only)` in `app/database/store.py` returns every row, one model, or only blocked attempts. The admin page at `/admin` sends those filters. The rows themselves are written by `save_held` and `save_confirmation`.
