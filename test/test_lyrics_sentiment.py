import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.lyrics_sentiment import sentiment_to_valence


def test_positive_text_has_high_valence():
    assert sentiment_to_valence("I am so happy and full of joy and love") > 0.6


def test_negative_text_has_low_valence():
    assert sentiment_to_valence("I feel so sad, hopeless and broken") < 0.4


def test_empty_text_is_neutral():
    assert sentiment_to_valence("") == 0.5
    assert sentiment_to_valence("   ") == 0.5
