# BugHound Mini Model Card (Reflection)

Fill this out after you run BugHound in **both** modes (Heuristic and Gemini).

---

# BugHound Model Card

## System Overview
BugHound is a cautious, agentic debugging assistant designed to analyze code,
propose minimal fixes, and defer to humans when confidence is low.

## Workflow
1. Analyze (heuristic or AI)
2. Propose fix
3. Assess risk
4. Decide or defer

## Reliability & Safety
BugHound defaults toward human review when:
- AI is involved
- AI disagrees with heuristics
- Risk exceeds threshold

## Observed Failure Modes
- AI output ambiguity
- Overconfidence without context

## Human-in-the-Loop Triggers
Any AI disagreement or elevated risk forces review.

## Proposed Improvement
Expand disagreement detection beyond count-based heuristics.