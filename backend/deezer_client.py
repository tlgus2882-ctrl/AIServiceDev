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


def search_tracks(query: str, limit: int = 8, timeout: int = 10) -> list:
    """자동완성용으로 곡 후보 목록을 가볍게 반환한다 (BPM 조회를 위한 추가 요청 없음).

    Deezer 검색 API는 `limit` 파라미터를 함께 보내면 결과가 0건으로 오는 경우가
    있어(재현 확인됨), limit은 보내지 않고 기본 응답을 잘라서 사용한다.
    """
    response = requests.get(_SEARCH_URL, params={"q": query}, timeout=timeout)
    response.raise_for_status()
    items = response.json().get("data", [])[:limit]
    return [
        {
            "id": item["id"],
            "title": item["title"],
            "artist": item["artist"]["name"],
            "album_cover": item.get("album", {}).get("cover_medium"),
        }
        for item in items
    ]
