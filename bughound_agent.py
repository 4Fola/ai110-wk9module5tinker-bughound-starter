import json
import re
from typing import Any, Dict, List, Optional, Tuple

from analyzers.heuristic_analyzer import HeuristicAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from fixers.heuristic_fixer import HeuristicFixer
from reliability.risk_assessor import assess_risk

class BugHoundAgent:
    """
    BugHound Agent

    Reliability-first, human-in-the-loop by design.
    """

    def __init__(self, mode: str = "heuristic"):
        self.mode = mode

        # WK09 Part 4 – Structured trace for UI and tests
        self.trace: List[Dict[str, str]] = []

        self.heuristic_analyzer = HeuristicAnalyzer()
        self.ai_analyzer = AIAnalyzer()
        self.heuristic_fixer = HeuristicFixer()

        self.ai_used = False
        self.ai_disagreed = False

    def _log(self, stage, source, status, message):
        """WK09 Part 4 – Centralized trace logging"""
        self.trace.append({
            "stage": stage,
            "source": source,
            "status": status,
            "message": message
        })

    def run(self, code: str) -> Dict[str, Any]:
        self.trace.clear()
        self.ai_used = False
        self.ai_disagreed = False

        self._log("ANALYZE", "SYSTEM", "INFO", "Starting analysis stage")
        analysis = self.analyze(code)

        self._log("FIX", "SYSTEM", "INFO", "Proposing fix")
        proposed_fix = self.propose_fix(code, analysis["final"])

        self._log("RISK", "SYSTEM", "INFO", "Assessing risk")
        risk_report = assess_risk(
            code,
            proposed_fix,
            ai_used=self.ai_used,
            ai_disagreed=self.ai_disagreed
        )

        # WK09 Part 4 – Hard autonomy lockout
        if self.ai_used and self.ai_disagreed:
            risk_report.should_autofix = False
            self._log(
                "DECIDE",
                "SYSTEM",
                "LOCKED",
                "AI disagreement forces human review"
            )
        else:
            self._log(
                "DECIDE",
                "SYSTEM",
                "INFO",
                f"auto_fix_allowed={risk_report.should_autofix}"
            )

        return {
            "issues_heuristic": analysis["heuristic"],
            "issues_ai": analysis["ai"],
            "issues_final": analysis["final"],
            "proposed_fix": proposed_fix,
            "risk_report": risk_report,
            "trace": self.trace,
        }

    def analyze(self, code: str) -> Dict[str, List[Dict[str, Any]]]:
        heuristic = self.heuristic_analyzer.analyze(code)
        self._log("ANALYZE", "HEURISTIC", "INFO", "Heuristic analysis complete")

        ai = []
        if self.mode == "gemini":
            self._log("ANALYZE", "AI", "INFO", "Attempting AI analysis")
            try:
                candidate = self.ai_analyzer.analyze(code)

                if not isinstance(candidate, list) or not candidate:
                    raise ValueError("Invalid AI output")

                if len(candidate) != len(heuristic):
                    self.ai_disagreed = True

                ai = candidate
                self.ai_used = True
                self._log("ANALYZE", "AI", "ACCEPTED", "AI output accepted")

            except Exception as e:
                self._log(
                    "ANALYZE",
                    "AI",
                    "REJECTED",
                    f"AI rejected: {str(e)}"
                )

        final = ai if ai and not self.ai_disagreed else heuristic

        if self.ai_disagreed:
            self._log(
                "ANALYZE",
                "SYSTEM",
                "INFO",
                "AI disagreement detected; heuristic preferred"
            )

        return {
            "heuristic": heuristic,
            "ai": ai,
            "final": final,
        }

    def propose_fix(self, code: str, issues: List[Dict[str, Any]]) -> str:
        self._log("FIX", "HEURISTIC", "INFO", "Applying conservative fix")
        return self.heuristic_fixer.fix(code, issues)

# WK09 Part 5 – Exportable trace for UI, logs, or grading
    def export_trace_json(self) -> str:
        import json
        return json.dumps(self.trace, indent=2)







