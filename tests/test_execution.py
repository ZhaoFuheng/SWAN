from swan_bench.execution import results_match


def test_unordered_rows_compare_as_sets():
    assert results_match([(1, "a"), (2, "b")], [(2, "b"), (1, "a")], ordered=False)
    assert not results_match([(1, "a")], [(1, "b")], ordered=False)


def test_ordered_rows_compare_in_order():
    assert results_match([(1,), (2,)], [(1,), (2,)], ordered=True)
    assert not results_match([(1,), (2,)], [(2,), (1,)], ordered=True)


def test_values_within_a_row_ignore_column_order():
    assert results_match([("x", 1)], [(1, "x")], ordered=True)


def test_row_counts_must_agree():
    assert not results_match([(1,)], [(1,), (1,)], ordered=False)


def test_floats_compare_to_ten_significant_digits():
    assert results_match([(0.1 + 0.2,)], [(0.3,)], ordered=False)
    assert results_match([(5.0,)], [(5,)], ordered=False)
    assert not results_match([(0.3001,)], [(0.3,)], ordered=False)
    assert results_match([(float("nan"),)], [(None,)], ordered=False)


def test_urls_compare_without_scheme_www_encoding_or_trailing_slash():
    assert results_match([("https://en.wikipedia.org/wiki/Mika_Häkkinen",)],
                         [("http://en.wikipedia.org/wiki/Mika_H%C3%A4kkinen",)], ordered=False)
    assert results_match([("https://www.Edline.net/pages/artesia_high_school/",)],
                         [("www.edline.net/pages/artesia_high_school",)], ordered=False)
    assert not results_match([("http://en.wikipedia.org/wiki/Monza",)], [("http://en.wikipedia.org/wiki/Imola",)], ordered=False)
    assert results_match([("plain text",)], [("plain text",)], ordered=False)
