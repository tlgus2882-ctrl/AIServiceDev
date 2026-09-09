"""곡 제목/아티스트를 입력받아 무드를 분석하는 API 서버."""
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

from backend import audio_energy, deezer_client, lyrics_client, lyrics_sentiment, mood_engine

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()
    if not query:
        return jsonify({"error": "query가 필요합니다."}), 400

    track = deezer_client.search_track(query)
    if track is None:
        return jsonify({"error": "곡을 찾을 수 없습니다."}), 404

    energy = 0.5
    if track.get("preview_url"):
        try:
            energy = audio_energy.analyze_preview_url(track["preview_url"])["energy"]
        except Exception:
            energy = 0.5

    lyrics_used = False
    valence = 0.5
    try:
        lyrics = lyrics_client.fetch_lyrics(track["title"], track["artist"])
        if lyrics:
            valence = lyrics_sentiment.sentiment_to_valence(lyrics)
            lyrics_used = True
    except RuntimeError:
        pass

    mood = mood_engine.classify_mood(valence=valence, energy=energy)

    return jsonify(
        {
            "track": {
                "title": track["title"],
                "artist": track["artist"],
                "bpm": track["bpm"],
                "album_cover": track["album_cover"],
            },
            "mood": mood,
            "lyrics_used": lyrics_used,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
