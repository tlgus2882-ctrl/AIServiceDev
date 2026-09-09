"""Deezer 공개 API로 곡을 검색한다. 인증이 필요 없다."""
import requests

_SEARCH_URL = "https://api.deezer.com/search"
_TRACK_URL = "https://api.deezer.com/track/{track_id}"


def get_track(track_id, timeout: int = 10) -> dict:
    response = requests.get(_TRACK_URL.format(track_id=track_id), timeout=timeout)
    response.raise_for_status()
    track = response.json()
    return {
        "id": track["id"],
        "title": track["title"],
        "artist": track["artist"]["name"],
        "bpm": track.get("bpm") or None,
        "preview_url": track.get("preview") or None,
        "album_cover": track.get("album", {}).get("cover_medium"),
    }


def search_track(query: str, timeout: int = 10):
    response = requests.get(_SEARCH_URL, params={"q": query}, timeout=timeout)
    response.raise_for_status()
    items = response.json().get("data", [])
    if not items:
        return None
    return get_track(items[0]["id"], timeout=timeout)
