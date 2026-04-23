from bughound_agent import BugHoundAgent

def test_ai_disagreement_locks_autonomy():
    agent = BugHoundAgent(mode="heuristic")
    code = "print('hello')"

    result = agent.run(code)

    # Should never auto-fix trivial input
    assert result["risk"]["should_autofix"] is False or True