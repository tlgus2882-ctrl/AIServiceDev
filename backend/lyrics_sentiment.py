"""가사 텍스트의 감성분석. VADER는 영어 위주라 한국어 가사에는 정확도가 낮을 수 있다."""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def sentiment_to_valence(text: str) -> float:
    """VADER의 compound score(-1~1)를 mood_engine이 쓰는 valence(0~1)로 변환한다."""
    if not text or not text.strip():
        return 0.5
    compound = _analyzer.polarity_scores(text)["compound"]
    return (compound + 1) / 2
