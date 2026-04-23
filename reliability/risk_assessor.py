# WK09 Part 3–5: Conservative risk assessment

class RiskReport:
    def __init__(self, risk_score, reasons, should_autofix):
        self.risk_score = risk_score
        self.reasons = reasons
        self.should_autofix = should_autofix


def assess_risk(original_code, fixed_code, issues, ai_used=False, ai_disagreed=False):
    reasons = []
    if fixed_code == "":
        reasons.append("No fix provided")
        return {"level": "high", "should_autofix": False, "score": 0, "reasons": reasons}
    
    has_high_severity = any(issue.get("severity") == "High" for issue in issues)
    if has_high_severity:
        reasons.append("High severity issues detected")
        return {"level": "high", "should_autofix": False, "score": 0, "reasons": reasons}
    
    if "return" in original_code and "return" not in fixed_code:
        reasons.append("Return statement removed")
    
    if original_code != fixed_code:
        reasons.append("Code was modified")
    
    return {"level": "low", "should_autofix": True, "score": 1, "reasons": reasons}

