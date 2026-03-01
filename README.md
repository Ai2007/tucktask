# Tuck Advisors – ABC Synergy API

A locally hosted REST API that serves and extends an AI-generated M&A synergy analysis for potential ABC buyers.

---

## Requirements

- Python 3.9+

---

## Setup

### 1. Install dependencies

```bash
.venv/bin/python -m pip install -r requirements.txt
```

### 2. Seed the database

Parses `input.json`, extracts the `gptOutput` markdown, and writes it to a local SQLite database (`analysis.db`).

```bash
.venv/bin/python seed.py
```

Expected output:
```
Database seeded successfully (~ characters written).
```

### 3. Start the API server

```bash
.venv/bin/uvicorn main:app --reload
```

The API is now live at `http://localhost:8000`.

---

## Endpoints

### `GET /analysis`

Returns the current markdown analysis string.

```bash
curl http://localhost:8000/analysis
```

**Response**

```json
{
  "markdown": "I will analyze ABC with Google Classroom as a buyer\n\n..."
}
```

---

### `POST /analysis`

Appends a string to the end of the existing markdown as a new sentence. The update is persisted in SQLite, so all subsequent GET or POST requests will reflect the change.

**Request body**

```json
{
  "content": "Your additional insight or note here."
}
```

**Example**

```bash
curl -X POST http://localhost:8000/analysis \
  -H "Content-Type: application/json" \
  -d '{"content": "Further diligence should focus on ABC revenue concentration risk."}'
```

**Response**

```json
{
  "markdown": "... [full updated markdown string]"
}
```

---

## Interactive Docs (Swagger UI)

FastAPI auto-generates an interactive docs page:

```
http://localhost:8000/docs
```

Use this to test both endpoints directly in the browser without needing curl.

---

## Project Structure

```
TuckAdvisors/
├── input.json        # GPT-generated synergy analysis (source of truth)
├── parser.py         # Extracts gptOutput markdown from input.json
├── database.py       # SQLite read/write helpers (analysis.db)
├── seed.py           # One-time script: parse input.json → write to DB
├── main.py           # FastAPI app with GET and POST /analysis endpoints
├── requirements.txt
└── README.md
```

---

## Design Notes

- **Persistence:** SQLite (`analysis.db`) is file-based and survives server restarts. The database holds exactly one row — the current markdown string — updated in place on every POST.
- **No in-memory state:** The server reads from and writes to SQLite on every request, so restarting the server never loses appended content.
- **Parser:** `parser.py` is intentionally kept as a pure extraction utility — it loads the JSON and returns the `gptOutput` string with no side effects, making it independently testable.
