# F.A.C.T — AI Fact-Checking & Analysis Tool v2.0

> **Submission for the [GitHub Finish-Up-A-Thon Challenge](https://dev.to/challenges/github-2026-05-21)**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![Gemini](https://img.shields.io/badge/Gemini-1.5--Flash-4285F4?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

F.A.C.T lets you type — or photograph — any claim, headline, or statement and get an instant, **sourced** verdict powered by Google Gemini with live Google Search grounding.

---

## ✨ What's New in v2.0

| | v1 (original) | v2 (this submission) |
|---|---|---|
| API route | `/api/analyze-text` ❌ broken | `/api/factcheck` ✅ fixed |
| Frontend → Backend | **Never connected** | Fully wired |
| Loading states | None | Rotating messages + animated dots |
| Result layout | Flat text dump | Two-panel, score ring (0–100) |
| Result history | None | Sidebar with one-click replay |
| OCR → Verify | Broken pipeline | One-click end-to-end |
| Error handling | Silent failures | Contextual user guidance |
| Retry logic | None | Exponential backoff (3 attempts) |
| Source display | Plain text | Favicon + hostname cards |
| Fingerprint | None | SHA-256 hash, copyable |
| Dark / Light mode | Broken CSS vars | Fully working toggle |

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/HarithaB2005/AI-Fact-Checker.git
cd AI-Fact-Checker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Gemini API key

Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)

```bash
# macOS / Linux
export GEMINI_API_KEY="your_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_key_here
```

### 4. Run the server

```bash
python app.py
```

### 5. Open in browser

```
http://localhost:5000
```

---

## 🗂 Project Structure

```
AI-Fact-Checker/
├── app.py              # Flask backend — Gemini API, grounding, fingerprint
├── index.html          # Frontend — two-panel UI, score ring, history, OCR
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Ignores venv, __pycache__, .env
```

---

## 🔍 How It Works

```
User types claim
      │
      ▼
Flask /api/factcheck
      │
      ▼
Gemini 1.5 Flash
  + Google Search grounding  ──► live web search
      │
      ▼
Structured JSON response
  { verdict, accuracy_score, analysis }
      │
      ▼
Extract groundingAttributions ──► sources []
      │
      ▼
Generate SHA-256 fingerprint
      │
      ▼
Return to frontend ──► render result card + score ring + source cards
```

**Image path:**
```
User uploads / drops image
      │
      ▼
Tesseract.js (in-browser OCR)
      │
      ▼
Extracted text injected into claim textarea
      │
      ▼
Same pipeline as above ──►
```

---

## 🛠 Tech Stack

- **Backend:** Python 3.9+, Flask 3.0, flask-cors
- **AI:** Google Gemini 1.5 Flash via REST API
- **Grounding:** Google Search (built into Gemini API)
- **OCR:** Tesseract.js 5 (runs entirely in the browser)
- **Frontend:** Vanilla HTML/CSS/JS — zero build step, zero frameworks

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google AI Studio API key |

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

## 🙏 Acknowledgements

- [Google AI Studio](https://aistudio.google.com) — Gemini API
- [Tesseract.js](https://github.com/naptha/tesseract.js) — In-browser OCR
- [GitHub Copilot](https://github.com/features/copilot) — Retry logic, schema generation, field-name catches
