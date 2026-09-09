"""미리듣기 오디오에서 RMS 음량 기반 에너지와 템포를 추정한다."""
import tempfile

import librosa
import numpy as np
import requests

# 실험적으로 관찰된 일반적인 RMS 범위(0~0.3)를 0~1로 스케일링하는 기준값.
_RMS_SCALE = 0.3


def estimate_energy(y) -> float:
    if y is None or len(y) == 0:
        return 0.5
    rms = librosa.feature.rms(y=y)[0]
    mean_rms = float(np.mean(rms))
    return float(np.clip(mean_rms / _RMS_SCALE, 0.0, 1.0))


def estimate_tempo(y, sr) -> float:
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return float(tempo)


def analyze_preview_url(preview_url: str, timeout: int = 10) -> dict:
    """libsndfile의 mp3 디코더는 실제 파일 경로가 필요해 임시 파일에 내려받은 뒤 읽는다."""
    response = requests.get(preview_url, timeout=timeout)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp_file:
        tmp_file.write(response.content)
        tmp_file.flush()
        y, sr = librosa.load(tmp_file.name, sr=None, mono=True)
    return {
        "energy": estimate_energy(y),
        "tempo": estimate_tempo(y, sr),
    }
