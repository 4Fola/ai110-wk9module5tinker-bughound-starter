# 🐶 BugHound

BugHound is a small, agentic debugging assistant for Python code.  
It analyzes code, proposes minimal fixes, evaluates risk, and decides whether
a fix should be auto‑applied or deferred to human review.

The system is intentionally cautious and designed to demonstrate how
agentic workflows, guardrails, and human‑in‑the‑loop decisions work in practice.

---

# I. Create env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# II. Install deps
pip install -r requirements.txt

# III. (Optional) Add Gemini key
cp .env.example .env
# add GEMINI_API_KEY=...

# IV. Run app
streamlit run bughound_app.py

# IVa. Run locally 
streamlit run bughound_app.py

# V. How To Run Tests
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

## Running Locally

### 1. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
