"""
Tests for ml/predictor.py
Covers clean_text() (pure function) and predict() (uses the committed model.pkl,
no database required).
"""

import pytest
from ml.predictor import clean_text, predict


def test_clean_text_lowercases():
    assert clean_text("HELLO World") == "hello world"


def test_clean_text_removes_urls():
    result = clean_text("Check this out http://example.com now")
    assert "http" not in result
    assert "example" not in result


def test_clean_text_removes_non_alpha_chars():
    result = clean_text("Breaking!!! News: 100% confirmed.")
    assert "!" not in result
    assert "100" not in result  # digits are stripped
    assert "breaking" in result


def test_clean_text_collapses_whitespace():
    result = clean_text("too    many     spaces")
    assert "  " not in result


def test_clean_text_handles_non_string_input():
    assert clean_text(None) == ""
    assert clean_text(12345) == ""


def test_predict_returns_expected_keys():
    result = predict("Some headline", "This is a fairly long piece of sample news text for testing purposes.")
    assert set(result.keys()) == {"prediction", "confidence", "fake_probability", "real_probability"}


def test_predict_label_matches_confidence():
    result = predict("Sample headline", "A reasonably long sample article body used purely for a CI test run.")
    assert result["prediction"] in ("FAKE", "REAL")
    if result["prediction"] == "FAKE":
        assert result["confidence"] == pytest.approx(result["fake_probability"])
    else:
        assert result["confidence"] == pytest.approx(result["real_probability"])


def test_predict_probabilities_sum_to_one():
    result = predict("Headline", "Another sample article body text used only for verifying probability output.")
    assert result["fake_probability"] + result["real_probability"] == pytest.approx(1.0, abs=1e-6)
