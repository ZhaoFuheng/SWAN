"""Few-shot examples for the BlendSQL baseline's LLMQA ingredient (from the 2024 notebook, typos fixed).

BlendSQL 0.1.x's LLMMap no longer takes retrieved few-shot examples (only one built-in example per return
type), so the 2024 per-database LLMMap example banks cannot be used and are not carried over; they remain in
the git history (`HybridQuery/BlendSQLSwanEval.ipynb`).
"""

LLMQA_EXAMPLES = [
    {
        "question": "Provide a list of super powers seperated by comma.",
        "context": {"hero": ["Abomination"]},
        "answer": "Accelerated Healing,Intelligence,Super Strength,Stamina,Super Speed,Invulnerability,"
                  "Animation,Super Breath",
    },
    {
        "question": "What is the skin colour?",
        "context": {"hero": ["Abin Sur"]},
        "answer": "Red",
    },
    {
        "question": "Provide the 3 letters short team name.",
        "context": {"long team name": ["Sporting Lokeren"]},
        "answer": "LOK",
    },
    {
        "question": "What is the player birthday (format: YYYY-MM-DD HH:MI:SS)?",
        "context": {"player name": ["Aaron Appindangoye"], "weight": [187]},
        "answer": "1992-02-29",
    },
    {
        "question": "Which country is the league from?",
        "context": {"league name": ["Manchester United"]},
        "answer": "England",
    },
    {
        "question": "What is the driver code",
        "context": {"driver name": ["LewisHamilton"]},
        "answer": "HAM",
    },
]
