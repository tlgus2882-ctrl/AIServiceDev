import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.audio_energy import estimate_energy


def test_silence_has_low_energy():
    silence = np.zeros(22050)
    assert estimate_energy(silence) < 0.1


def test_loud_signal_has_high_energy():
    t = np.linspace(0, 1, 22050)
    loud = 0.9 * np.sin(2 * np.pi * 440 * t)
    assert estimate_energy(loud) > 0.5


def test_empty_array_is_neutral():
    assert estimate_energy(np.array([])) == 0.5
