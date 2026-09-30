-- LLMQA over the two-row UNION with options=colour.colour; UNION sorts in sqlite, so the list is ordered
SELECT ai_agg(list('superhero_name: ' || superhero_name ORDER BY superhero_name),
              'What is the colour of Apocalypses skin? Answer with exactly one of: '
              || (SELECT string_agg(DISTINCT colour, ', ' ORDER BY colour) FROM colour) || '.')
FROM (SELECT 'Apocalypses' AS superhero_name
      UNION
      SELECT superhero_name FROM superhero AS T1 WHERE T1.superhero_name = 'Apocalypse')
