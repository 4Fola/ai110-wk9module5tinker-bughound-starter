# 🐶 BugHound
# 👉 [ReadMe](README.md) | [Model Card](model_card.md) |

BugHound is a small, agentic debugging assistant for Python code.  
It analyzes code, proposes minimal fixes, evaluates risk, and decides whether
a fix should be auto‑applied or deferred to human review.

The system is intentionally cautious and designed to demonstrate how
agentic workflows, guardrails, and human‑in‑the‑loop decisions work in practice.

---

<img src="assets/BugHound-Demo.gif" alt="BugHound-Demo">

I. **Create env**
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

II. **Install deps**
pip install -r requirements.txt

III. **(Optional) Add Gemini key**
cp .env.example .env
 **add GEMINI_API_KEY=...**

IV. **Run app locally**
streamlit run bughound_app.py

V. **How To Run Tests**
pytest tests/

## What BugHound Does

Given a short Python snippet, BugHound:

1. **Analyzes the code**
   - Uses heuristic rules in offline mode
   - Optionally uses Gemini for AI‑assisted analysis

2. **Proposes a fix**
   - Prioritizes minimal, behavior‑preserving changes
   - Defaults to conservative heuristic fixes

3. **Assesses risk**
   - Scores changes based on safety signals
   - Increases caution when AI is involved

4. **Decides or defers**
   - Auto‑fixes only when confidence is high
   - Locks autonomy and requires human review when risk is elevated

5. **Shows its reasoning**
   - Displays detected issues
   - Shows proposed fixes
   - Logs each agent decision step
   - Allows export of the full agent trace as JSON

---

<img src="assets/BugHound_Agent_Workflow.jpg" alt="BugHound_Agent_Workflow">

## Running Locally

### 1. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows

Example Codes to paste: SCENARIO 1 — Heuristic Mode (Offline, No AI)

def greet(name):
    print("Hello", name)
    return True
   
✅ Expected behavior

✅ Only heuristic analysis runs
✅ Trace shows NO AI entries
✅ Fix may adjust formatting or flag style issues

Example Codes to paste: SCENARIO 2 — Gemini Accepted (AI Helps)

def load_data(path):
    try:
        data = open(path).read()
    except:
        return None
    return data

✅ Expected behavior

✅ Gemini runs
✅ AI output is valid
✅ AI issues may differ from heuristics
✅ If no disagreement → AI accepted

Example Codes to paste: SCENARIO 3 — Gemini Rejected (Fallback Works)
# This is intentionally simple
x = 1

✅ Expected behavior

✅ Gemini may return malformed / empty output
✅ Agent rejects it
✅ Heuristics are used instead

Example Codes to paste: SCENARIO 4 — AI Disagreement → Autonomy Lockout
def divide(a, b):
    try:
        return a / b
    except:
        return 0

✅ Expected behavior

✅ AI finds different issues than heuristics
✅ Disagreement detected
✅ Auto‑fix disabled

Example Codes to paste: SCENARIO 5 — Export Trace JSON
✅ Expected JSON shape
[
  {
    "stage": "ANALYZE",
    "source": "AI",
    "status": "ACCEPTED",
    "message": "AI output accepted"
  },
  {
    "stage": "DECIDE",
    "source": "SYSTEM",
    "status": "LOCKED",
    "message": "AI disagreement forces human review"
  }
]


