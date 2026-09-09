"""곡 제목/아티스트를 입력받아 무드를 분석하는 API 서버."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

from backend import audio_energy, deezer_client, lyrics_client, lyrics_sentiment, mood_engine

# 자동완성 후보마다 가사 확보 여부를 확인해야 해서 병렬로 조회한다.
_SUGGESTION_POOL_SIZE = 15
_SUGGESTION_RESULT_LIMIT = 8

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/search")
def search():
    query = (request.args.get("q") or "").strip()
    if len(query) < 2:
        return jsonify({"results": []})

    candidates = deezer_client.search_tracks(query, limit=_SUGGESTION_POOL_SIZE)
    with ThreadPoolExecutor(max_workers=8) as executor:
        lyrics_found = executor.map(
            lambda track: lyrics_client.has_lyrics(track["title"], track["artist"]), candidates
        )
    results = [track for track, found in zip(candidates, lyrics_found) if found]
    return jsonify({"results": results[:_SUGGESTION_RESULT_LIMIT]})


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    track_id = payload.get("track_id")
    query = (payload.get("query") or "").strip()

    if track_id:
        track = deezer_client.get_track(track_id)
    elif query:
        track = deezer_client.search_track(query)
    else:
        return jsonify({"error": "query 또는 track_id가 필요합니다."}), 400

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
    lyrics = lyrics_client.fetch_lyrics(track["title"], track["artist"])
    if lyrics:
        valence = lyrics_sentiment.sentiment_to_valence(lyrics)
        lyrics_used = True

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
    # macOS는 5000번 포트를 AirPlay 수신 기능이 기본으로 사용해 충돌(403)이 나므로 5050을 쓴다.
    app.run(debug=True, port=5050)
