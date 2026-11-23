# Dillon

The prompt log is no longer a stub. Every submitted prompt is stored in `data/shadow.db` and shown on the password-protected admin page (`/admin`).

`app/database/store.py` already implements `save_held`, `save_confirmation`, and `flagged_report`. Do not replace those with a second database or the admin page will split into two logs.

A useful follow-up, if you still want a piece of your own: add a filter on the admin log (by model, or only rows that were blocked). The page already renders whatever `flagged_report()` returns.
