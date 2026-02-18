# The Cortex — Personal Knowledge Base Engine

Reads, reasons, organizes, expands, remembers, and converses over your personal knowledge.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional but recommended for richer summaries/chat:

```bash
export OPENAI_API_KEY="your_key_here"
```

## Run

```bash
python cortex.py --help
```

## Core Commands

```bash
python cortex.py ingest <file_or_url_or_note>
python cortex.py search "your question here"
python cortex.py expand
python cortex.py explore <topic>
python cortex.py tags
python cortex.py stats
python cortex.py related <entry_id>
python cortex.py chat
python cortex.py repair [--reingest/--no-reingest] [--quiet] [--json]
```

## Feeds

```bash
python cortex.py feeds add <url> [--tag TAG] [--name NAME]
python cortex.py feeds list
python cortex.py feeds pull
python cortex.py feeds remove <feed_id>
```

## Export

```bash
python cortex.py export obsidian [--dir DIR]
python cortex.py export json [--file FILE]
```

## Automation

```bash
python cortex.py daemon
scripts/repair-cron.sh
```

## Dashboard UI

```bash
export CORTEX_DASH_SECRET="change-this-secret"
export CORTEX_DASHBOARD_PASSWORD="optional-shared-password" # optional but recommended
export GHOSTLINE_BASE_URL="http://ghostline.boo"
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
export CORTEX_SSO_STRICT="true" # disables local login when Google SSO is configured
# optional override if behind reverse proxy
# export CORTEX_OAUTH_REDIRECT_URI="https://your-host/auth/google/callback"
uvicorn dashboard:app --host 0.0.0.0 --port 8787 --reload
```

Access:

- Open `http://localhost:8787/login`
- Google SSO is supported and restricted to verified `@ghostline.boo` accounts
- Local login fallback is also restricted to `@ghostline.boo` email addresses
- Set `CORTEX_SSO_STRICT=true` to allow only Google SSO (no local form login)
- In strict mode, startup fails fast if Google OAuth credentials are missing
- If `CORTEX_DASHBOARD_PASSWORD` is set, password is required in addition to email domain

## Storage

The engine stores everything under:

- `~/.cortex/cortex.db` (SQLite metadata)
- `~/.cortex/vectors` (Chroma vector store)
- `~/.cortex/exports` (JSON exports)
- `~/.cortex/obsidian_vault` (Obsidian vault exports)

## Notes

- If `sentence-transformers` or `chromadb` are missing, search gracefully degrades.
- If `openai` or `OPENAI_API_KEY` is missing, summarization/chat fall back to local logic.
- Web expansion and URL ingestion need `requests` and `beautifulsoup4`.
- For production dashboard security, run behind HTTPS and set a strong `CORTEX_DASH_SECRET`.
- Set `CORTEX_DASH_HTTPS_ONLY=true` in production to enforce secure session cookies.
