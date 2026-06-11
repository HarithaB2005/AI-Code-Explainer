import os
import requests
import json
import time
import hashlib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__, static_folder=".")
CORS(app)

# --- Configuration ---
# Set your Gemini API key as an environment variable: export GEMINI_API_KEY="your_key_here"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Using the stable gemini-1.5-flash model (gemini-2.5-flash-preview had a wrong date suffix before)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


def call_gemini_api_with_retry(url, key, payload, max_retries=3):
    """POST to Gemini API with exponential backoff for transient errors."""
    headers = {"Content-Type": "application/json"}
    url_with_key = f"{url}?key={key}"
    for attempt in range(max_retries):
        try:
            response = requests.post(url_with_key, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise e
    return None


def generate_fingerprint(claim: str, verdict: str, score: int) -> str:
    """Generate a short SHA-256 fingerprint for a fact-check result."""
    raw = f"{claim.strip().lower()}|{verdict.lower()}|{score}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


# ---------------------------------------------------------------
# FIX: The old frontend called /api/analyze-text but the backend
#      only had /api/factcheck — both routes now point here.
# ---------------------------------------------------------------
@app.route("/api/factcheck", methods=["POST"])
@app.route("/api/analyze-text", methods=["POST"])  # legacy alias kept for compatibility
def fact_check_claim():
    """
    Accept a claim and return:
      - verdict       : "True" | "False" | "Partially True"
      - accuracy_score: 0–100
      - analysis      : concise paragraph
      - sources       : list of {title, uri, hostname}
      - fingerprint   : short hash for sharing / archiving
    """
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "GEMINI_API_KEY environment variable is not set. "
                     "Run: export GEMINI_API_KEY='your_key_here'"
        }), 500

    try:
        data = request.get_json()
        # Support both field names from old and new frontend
        claim = data.get("claim") or data.get("text", "").strip()

        if not claim:
            return jsonify({"error": "Missing 'claim' field in request body"}), 400

        if len(claim) > 2000:
            return jsonify({"error": "Claim must be under 2000 characters"}), 400

        system_prompt = (
            "You are a world-class fact-checker. Use the provided Google Search results "
            "to assess the accuracy of the user's claim. "
            "Respond STRICTLY in the requested JSON format. "
            "accuracy_score (0-100) is your confidence in the verdict based on found sources."
        )

        payload = {
            "contents": [{"parts": [{"text": f"Fact-Check this claim: {claim}"}]}],
            "tools": [{"google_search": {}}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "verdict": {
                            "type": "STRING",
                            "description": "Exactly one of: 'True', 'False', 'Partially True'."
                        },
                        "accuracy_score": {
                            "type": "INTEGER",
                            "description": "Confidence in the verdict from 0 to 100."
                        },
                        "analysis": {
                            "type": "STRING",
                            "description": "2-3 sentences explaining the verdict using retrieved sources."
                        }
                    },
                    "propertyOrdering": ["verdict", "accuracy_score", "analysis"]
                }
            }
        }

        response = call_gemini_api_with_retry(API_URL, GEMINI_API_KEY, payload)
        gemini_result = response.json()

        candidate = gemini_result.get("candidates", [None])[0]
        if not candidate:
            return jsonify({"error": "Gemini returned an empty response."}), 500

        json_text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        try:
            result_data = json.loads(json_text)
        except json.JSONDecodeError:
            app.logger.error(f"Malformed JSON from Gemini: {json_text}")
            return jsonify({"error": "API returned malformed JSON.", "raw": json_text}), 500

        # Extract grounding sources
        sources = []
        grounding = candidate.get("groundingMetadata", {})
        attributions = grounding.get("groundingAttributions", [])
        for attr in attributions:
            web = attr.get("web", {})
            uri = web.get("uri", "")
            title = web.get("title", "")
            if uri and title:
                sources.append({
                    "title": title,
                    "uri": uri,
                    "hostname": urlparse(uri).hostname or "unknown"
                })

        # Build final response
        result_data["sources"] = sources
        result_data["fingerprint"] = generate_fingerprint(
            claim,
            result_data.get("verdict", "unknown"),
            result_data.get("accuracy_score", 0)
        )

        return jsonify(result_data)

    except requests.exceptions.HTTPError as e:
        app.logger.error(f"Gemini HTTP error: {e}. Body: {e.response.text}")
        return jsonify({"error": "Gemini API request failed.", "details": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected server error.", "details": str(e)}), 500


# Serve the frontend from the same directory
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("\n⚠  WARNING: GEMINI_API_KEY not set.")
        print("   Run: export GEMINI_API_KEY='your_key_here'\n")
    app.run(host="0.0.0.0", debug=False, port=5000)
