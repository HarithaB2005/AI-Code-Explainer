# I Built an AI Fact-Checker That Never Actually Worked — Until Now

*This is a submission for the [GitHub Finish-Up-A-Thon Challenge](https://dev.to/challenges/github-2026-05-21)*

---

## What I Built

**F.A.C.T** (Fact-Checking & Analysis Tool) is an AI-powered web application that lets you type — or photograph — any claim, headline, or piece of text and get an instant, sourced verdict on whether it's true, false, or somewhere in between.

Under the hood, it uses **Google's Gemini 1.5 Flash** model with live **Google Search grounding** — meaning the AI doesn't just guess from training data, it actively searches the web in real-time and returns the actual sources it used. You get a verdict, a confidence score (0–100), a plain-English analysis, clickable source links, and a unique fingerprint hash for every result so you can share or archive checks.

The image analysis path uses **Tesseract.js** for in-browser OCR — point your camera at a newspaper headline or screenshot a tweet, and the extracted text flows straight into the fact-checking pipeline.

It's the kind of tool I genuinely wish existed when I was doom-scrolling misinformation during exam season.

---

## Demo

{% embed https://github.com/HarithaB2005/AI-Fact-Checker %}

**Live flow:**

1. Type a claim like *"The Great Wall of China is visible from space"*
2. Hit **Verify Claim** (or Ctrl+Enter)
3. Watch the Gemini API search the web live
4. Get back: `False · 12/100 · "No human eye can resolve the wall's width from low Earth orbit…"` with BBC, NASA, and Snopes as sources
5. Check History tab to replay any previous result

**Screenshots:**

> _Cover image: Two-panel UI — input left, result right, score ring showing 12/100 for the Great Wall myth_

---

## The Comeback Story

Here's the embarrassing truth I'm happy to finally say out loud.

I built the first version of this during a hackathon sprint sometime last year. The idea was solid. The Gemini integration was actually working. I had a Flask backend with Google Search grounding, a Tesseract OCR path for images, even a dark mode toggle. I pushed it, called it done, and moved on.

Except it was **completely broken** and I didn't realise until I came back to it for this challenge.

### The Bug That Killed Everything

Open `index.html` from the original repo. Find the fetch call. It says:

```javascript
// v1 — BROKEN
const resp = await fetch("/api/analyze-text", { ... });
```

Now open `app.py`. Search for that route. It isn't there.

```python
# v1 — app.py only had this
@app.route("/api/factcheck", methods=["POST"])
def fact_check():
    ...
```

Two files. Two different route names. The frontend and backend had **never talked to each other**. Every single "demo" I thought I had was just the loading spinner spinning forever before silently dying. The app had a beautiful frontend and a working backend that had never once shaken hands.

That's the before. A perfectly broken app, confidently pushed to GitHub.

### What I Actually Fixed and Built

**🔴 Critical fix — the route disconnect:**

```python
# v2 — both routes now work
@app.route("/api/factcheck", methods=["POST"])
@app.route("/api/analyze-text", methods=["POST"])  # legacy alias
def fact_check_claim():
    ...
```

```javascript
// v2 — frontend now calls the right endpoint
const resp = await fetch("/api/factcheck", { ... });
```

**🟡 Backend hardening:**

- Added exponential backoff retry logic (`call_gemini_api_with_retry`) — the original would crash on any transient Gemini error
- Switched to `responseMimeType: "application/json"` with a strict response schema — no more fragile string parsing
- Added `generate_fingerprint()` — SHA-256 hash of claim + verdict + score, returned on every result for sharing
- Proper source extraction from `groundingMetadata.groundingAttributions`
- Startup warning if `GEMINI_API_KEY` isn't set (you'd just get a silent 500 before)
- Input validation — length cap, empty claim check, field aliasing for both `claim` and `text`

**🟢 Frontend rewrite:**

| Feature | v1 | v2 |
|---|---|---|
| API route | `/api/analyze-text` ❌ | `/api/factcheck` ✅ |
| Loading states | None | Rotating messages + dots |
| Result layout | Flat text dump | Two-panel, score ring |
| History | None | Sidebar with replay |
| OCR → Verify | Broken pipeline | One-click end-to-end |
| Error messages | Silent failure | Contextual guidance |
| Fingerprint | None | Displayed + copyable |
| Sources | Listed as plain text | Favicon + hostname cards |
| Theme | Broken CSS vars | Working dark/light toggle |

---

## My Experience with GitHub Copilot

I'll be honest — I used GitHub Copilot for exactly the parts where I needed it most: the tedious structural work that wasn't interesting to type but was critical to get right.

**Where it actually helped:**

When I was writing the retry wrapper for the Gemini API, I typed the function signature and the first `try` block, and Copilot autocompleted the entire exponential backoff pattern correctly — `2 ** attempt` delay, proper re-raise on the final attempt, the works. That's maybe 15 lines I didn't have to think about.

The response schema for Gemini's structured output took some back-and-forth. I described what I wanted in a comment — `# return verdict, score 0-100, analysis as strict JSON` — and Copilot generated the `responseSchema` dict. It got the `propertyOrdering` field wrong on the first pass (it doesn't exist in the v1beta spec), and I had to correct it, but that's the honest Copilot experience: it gets you 80% there and you validate the other 20%.

For the frontend score ring SVG, I described the visual I wanted in a comment above an empty function and Copilot drew the circle math. That one I kept nearly verbatim.

The most useful Copilot moment was the least glamorous: it caught that I'd written `data.accuracy` in the frontend when the backend was returning `data.accuracy_score`. Tiny field name mismatch, the kind of thing that would have cost me 20 minutes of console.log debugging. Copilot's inline suggestion flagged it by autocompleting to `accuracy_score` when I started typing `data.a`.

What Copilot *couldn't* do was find the original bug — the route disconnect was a cross-file semantic issue, not a syntax problem. That one I had to trace manually by actually reading both files side by side. But once I knew what to fix, Copilot made the fix fast.

---

*If you've ever pushed a project that "works" and then found out months later it never did — drop a comment. I know I'm not alone.*
