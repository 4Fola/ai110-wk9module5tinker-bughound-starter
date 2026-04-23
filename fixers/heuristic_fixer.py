import re

class HeuristicFixer:
    def fix(self, code: str, issues):
        if any(issue.get("msg") == "print" for issue in issues):
            # Add import logging if not present
            if "import logging" not in code:
                code = "import logging\n" + code
            # Replace print( with logging.info(
            code = re.sub(r'print\(', 'logging.info(', code)
        return code