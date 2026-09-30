{{
LLMQA(
    'Provide the 3 letters short team name',
    (SELECT Team.team_long_name FROM Team
        WHERE Team.team_long_name = 'Queens Park Rangers'
    )
)
}}
