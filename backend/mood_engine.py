"""valence(긍정-부정)와 energy(에너지)를 12방향 무드 휠에 매핑한다.

무드 휠은 (valence=0.5, energy=0.5)를 중심으로 한 원 위에 30도 간격으로
12개의 무드를 배치한 것이다. 순수 긍정(valence=1, energy=0.5)이 0도(Happy),
순수 고에너지(valence=0.5, energy=1)가 90도(Tense)가 되도록 정렬했다.
"""
import math

MOOD_WHEEL = [
    ("Happy", "행복"),
    ("Excited", "신남"),
    ("Passionate", "열정"),
    ("Tense", "긴장"),
    ("Angry", "분노"),
    ("Aggressive", "격렬함"),
    ("Sad", "슬픔"),
    ("Melancholic", "우울"),
    ("Lonely", "쓸쓸함"),
    ("Calm", "평온"),
    ("Relaxed", "편안함"),
    ("Content", "포근함"),
]


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def classify_mood(valence: float, energy: float) -> dict:
    v = _clamp01(valence)
    e = _clamp01(energy)
    angle = math.degrees(math.atan2(e - 0.5, v - 0.5)) % 360
    index = int(((angle + 15) % 360) // 30)
    mood_en, mood_ko = MOOD_WHEEL[index]
    return {
        "mood_en": mood_en,
        "mood_ko": mood_ko,
        "valence": v,
        "energy": e,
        "angle_deg": round(angle, 1),
    }
