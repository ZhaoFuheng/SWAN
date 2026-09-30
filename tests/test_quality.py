"""SemBench-style quality: relative error for a single number, set F1 for rows."""

from swan_bench.quality import metric_kind, quality


def test_single_number_scores_by_relative_error():
    assert metric_kind([(10,)]) == "aggregate"
    assert quality([(9,)], [(10,)], "SELECT COUNT(*) FROM t")["quality"] == 0.9
    assert quality([(30,)], [(10,)], "SELECT COUNT(*) FROM t")["quality"] == 0.0
    assert quality([("12.5",)], [(10,)], "q")["quality"] == 0.75
    assert quality([(0,)], [(0,)], "q")["quality"] == 1.0
    assert quality([(1,)], [(0,)], "q")["quality"] == 0.0
    assert quality([(9,), (10,)], [(10,)], "q")["quality"] == 0.0  # must be one row


def test_rows_score_by_set_f1():
    gold = [("a",), ("b",), ("c",), ("d",)]
    assert metric_kind(gold) == "rows" and metric_kind([("x",)]) == "rows" and metric_kind([(1, "x")]) == "rows"
    r = quality([("a",), ("b",), ("z",)], gold, "SELECT x FROM t")
    assert (r["precision"], r["recall"]) == (0.6667, 0.5) and r["quality"] == 0.5714
    assert quality([(1, "x")], [("x", 1)], "q")["quality"] == 1.0  # column order does not matter


def test_limit_counts_only_the_first_k_system_rows():
    gold = [("a",), ("b",)]
    assert quality([("a",), ("b",), ("c",)], gold, "SELECT x FROM t ORDER BY y LIMIT 2")["quality"] == 1.0
    assert quality([("c",), ("a",), ("b",)], gold, "SELECT x FROM t ORDER BY y LIMIT 2")["quality"] == 0.5


def test_empty_results():
    assert quality([], [], "q")["quality"] == 1.0
    assert quality([], [("a",)], "q")["quality"] == 0.0
    assert quality([("a",)], [], "q")["quality"] == 0.0
