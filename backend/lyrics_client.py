"""Genius API로 가사를 가져온다. GENIUS_ACCESS_TOKEN 환경변수가 필요하다."""
import os

import lyricsgenius

_genius = None


def _get_client():
    global _genius
    if _genius is None:
        token = os.environ.get("GENIUS_ACCESS_TOKEN")
        if not token:
            raise RuntimeError("GENIUS_ACCESS_TOKEN 환경변수가 설정되어 있지 않습니다.")
        _genius = lyricsgenius.Genius(token, verbose=False, remove_section_headers=True)
    return _genius


def fetch_lyrics(title: str, artist: str):
    genius = _get_client()
    song = genius.search_song(title, artist)
    return song.lyrics if song else None
