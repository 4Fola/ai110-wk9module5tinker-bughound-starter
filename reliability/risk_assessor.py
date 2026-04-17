from typing import Dict, List

# WK09 Part 5 – Minimal RiskReport definition (missing import fix)

class RiskReport:
    def __init__(self, risk_score, reasons, should_autofix):
        self.risk_score = risk_score
        self.reasons = reasons
        self.should_autofix = should_autofix


def assess_risk(original_code, proposed_code, ai_used=False, ai_disagreed=False):
    risk_score = 0
    reasons = []

    if original_code != proposed_code:
        risk_score += 1
        reasons.append("Code changes detected")

    # WK09 Part 4 – AI always increases caution
    if ai_used:
        risk_score += 1
        reasons.append("AI-assisted change")

    # WK09 Part 4 – Disagreement is a red flag
    if ai_disagreed:
        risk_score += 1
        reasons.append("AI and heuristic disagreement")

    should_autofix = risk_score < 2

    return RiskReport(
        risk_score=risk_score,
        reasons=reasons,
        should_autofix=should_autofix
    )
