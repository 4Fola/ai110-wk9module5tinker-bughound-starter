class HeuristicAnalyzer:
    def analyze(self, code: str):
        issues = []
        if "print(" in code:
            issues.append({"type": "Code Quality", "severity": "Low", "msg": "print"})
        return issues