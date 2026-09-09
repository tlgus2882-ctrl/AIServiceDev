import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.mood_engine import MOOD_WHEEL, classify_mood


def test_pure_positive_valence_is_happy():
    result = classify_mood(valence=1.0, energy=0.5)
    assert result["mood_en"] == "Happy"


def test_pure_negative_valence_is_sad():
    result = classify_mood(valence=0.0, energy=0.5)
    assert result["mood_en"] == "Sad"


def test_pure_high_energy_is_tense():
    result = classify_mood(valence=0.5, energy=1.0)
    assert result["mood_en"] == "Tense"


def test_pure_low_energy_is_calm():
    result = classify_mood(valence=0.5, energy=0.0)
    assert result["mood_en"] == "Calm"


def test_all_wheel_labels_reachable():
    seen = set()
    steps = 36
    for i in range(steps):
        angle = i * (360 / steps)
        v = 0.5 + 0.5 * math.cos(math.radians(angle))
        e = 0.5 + 0.5 * math.sin(math.radians(angle))
        seen.add(classify_mood(v, e)["mood_en"])
    assert seen == {mood_en for mood_en, _ in MOOD_WHEEL}


def test_values_are_clamped():
    result = classify_mood(valence=1.5, energy=-0.5)
    assert result["valence"] == 1.0
    assert result["energy"] == 0.0
