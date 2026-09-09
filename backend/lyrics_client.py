"""가사 텍스트 확보. Genius를 우선 시도하고, 못 찾으면 lyrics.ovh로 재시도한다.

같은 (title, artist) 조합은 자동완성 필터링과 실제 분석에서 중복 조회되므로
lru_cache로 캐싱해 불필요한 네트워크 호출을 줄인다.
"""
import os
import threading
from functools import lru_cache

import lyricsgenius
import requests

_genius = None
_genius_lock = threading.Lock()


def _get_genius_client():
    global _genius
    if _genius is None:
        with _genius_lock:
            if _genius is None:
                token = os.environ.get("GENIUS_ACCESS_TOKEN")
                if not token:
                    return None
                _genius = lyricsgenius.Genius(token, verbose=False, remove_section_headers=True)
    return _genius


def _fetch_from_genius(title: str, artist: str):
    genius = _get_genius_client()
    if genius is None:
        return None
    try:
        song = genius.search_song(title, artist)
    except Exception:
        return None
    return song.lyrics if song else None


def _fetch_from_lyrics_ovh(title: str, artist: str, timeout: int = 8):
    try:
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{title}", timeout=timeout)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.json().get("lyrics") or None


@lru_cache(maxsize=256)
def fetch_lyrics(title: str, artist: str):
    return _fetch_from_genius(title, artist) or _fetch_from_lyrics_ovh(title, artist)


def has_lyrics(title: str, artist: str) -> bool:
    return fetch_lyrics(title, artist) is not None
