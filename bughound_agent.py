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

    Cautious debugging assistant with human-in-the-loop bias.
    """

    def __init__(self, mode: str = "heuristic"):
        self.mode = mode
        self.trace: List[str] = []

        self.heuristic_analyzer = HeuristicAnalyzer()
        self.ai_analyzer = AIAnalyzer()
        self.heuristic_fixer = HeuristicFixer()

        # WK09 Part 3 – Track AI usage for risk decisions
        self.ai_used = False

    def run(self, code: str) -> Dict[str, Any]:
        self.trace.clear()
        self.ai_used = False

        self.trace.append("[ANALYZE] Starting issue detection")
        analysis_result = self.analyze(code)

        self.trace.append("[FIX] Proposing candidate fix")
        proposed_fix = self.propose_fix(code, analysis_result["final"])

        self.trace.append("[RISK] Assessing change safety")
        risk_report = assess_risk(
            code,
            proposed_fix,
            ai_used=self.ai_used  # WK09 Part 3 – bias toward caution
        )

        self.trace.append(
            f"[DECIDE] auto_fix_allowed={risk_report.should_autofix}"
        )

        return {
            # WK09 Part 3 – Side-by-side comparison for UI
            "issues_heuristic": analysis_result["heuristic"],
            "issues_ai": analysis_result["ai"],
            "issues_final": analysis_result["final"],
            "proposed_fix": proposed_fix,
            "risk_report": risk_report,
            "trace": self.trace,
        }

    def analyze(self, code: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Runs heuristic analysis first.
        AI is optional and strictly validated.
        """

        heuristic_issues = self.heuristic_analyzer.analyze(code)
        self.trace.append("[ANALYZE][HEURISTIC] Issues detected")

        ai_issues: List[Dict[str, Any]] = []

        if self.mode == "gemini":
            self.trace.append("[ANALYZE][AI] Attempting AI analysis")

            try:
                candidate = self.ai_analyzer.analyze(code)

                # WK09 Part 3 – Even stricter AI rejection
                if (
                    not isinstance(candidate, list)
                    or not candidate
                    or abs(len(candidate) - len(heuristic_issues)) > 2
                ):
                    raise ValueError("AI output confidence too low")

                ai_issues = candidate
                self.ai_used = True
                self.trace.append("[ANALYZE][AI][ACCEPTED] Output validated")

            except Exception as e:
                self.trace.append(
                    f"[ANALYZE][AI][REJECTED] {str(e)}"
                )

        # WK09 Part 3 – Default to safer result
        final_issues = ai_issues if ai_issues else heuristic_issues

        return {
            "heuristic": heuristic_issues,
            "ai": ai_issues,
            "final": final_issues,
        }

    def propose_fix(self, code: str, issues: List[Dict[str, Any]]) -> str:
        self.trace.append("[FIX][HEURISTIC] Applying conservative fixer")
        return self.heuristic_fixer.fix(code, issues)
    

    