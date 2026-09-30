"""The one-off 2024 -> BlendSQL 0.1.x query translation (scripts/blendsql_2024_syntax.py)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from blendsql_2024_syntax import semicolon_options, translate  # noqa: E402


def test_column_strings_become_references():
    assert translate("{{LLMMap('q?', 'circuits::location')}}") == "{{LLMMap('q?', circuits.location)}}"
    assert translate("{{LLMMap('q?', (superhero::superhero_name))}}") == "{{LLMMap('q?', superhero.superhero_name)}}"
    assert translate("{{LLMMap('q?', 'a::b', options='publisher::publisher_name')}}") == \
        "{{LLMMap('q?', a.b, options=publisher.publisher_name)}}"


def test_missing_comma_is_added():
    assert translate("{{LLMMap('Is it?' 'T1::name')}}") == "{{LLMMap('Is it?', T1.name)}}"


def test_temp_cte_is_renamed_outside_strings():
    out = translate("WITH temp AS (SELECT 'temp' AS x FROM t) SELECT temp.x FROM temp")
    assert out == "WITH temp_cte AS (SELECT 'temp' AS x FROM t) SELECT temp_cte.x FROM temp_cte"


def test_ingredient_uses_the_alias():
    out = translate("SELECT 1 FROM schools AS T2 WHERE {{LLMMap('q?', 'schools::Street')}} = TRUE")
    assert out == "SELECT 1 FROM schools AS T2 WHERE {{LLMMap('q?', T2.Street)}} = TRUE"


def test_semicolon_options_become_a_tuple():
    assert semicolon_options("LLMMap('q?', t.c, options='A b;C')") == "LLMMap('q?', t.c, options=('A b', 'C'))"
    assert semicolon_options("options=('A','B')") == "options=('A','B')"
