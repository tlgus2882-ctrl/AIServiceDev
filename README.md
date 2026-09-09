# AIServiceDev

인공지능서비스개발II 프로젝트. 현재 곡의 가사와 BPM 등 오디오 정보를 이용해
분위기(무드)를 분석하는 서비스를 개발 중이다.

## 음악 분위기 분석기

- Deezer 공개 API로 곡을 검색해 BPM과 미리듣기(30초) URL을 가져온다.
- 미리듣기 오디오를 librosa로 분석해 에너지(RMS 음량)를 추정한다.
- Genius API로 가사를 가져와 감성분석(VADER)으로 valence(긍정/부정)를 추정한다.
- valence·energy를 12방향 무드 휠(mood wheel)에 매핑해 최종 분위기를 정한다.

### 준비

```bash
pip install -r requirements.txt
cp .env.example .env
# .env에 GENIUS_ACCESS_TOKEN 입력 (https://genius.com/api-clients 에서 발급)
```

### 실행

```bash
python -m backend.app
```

브라우저에서 http://localhost:5050 접속.
(macOS는 5000번 포트를 AirPlay 수신 기능이 기본으로 점유해 403 에러가 나기 때문에 5050번을 사용한다.
필요하면 시스템 설정 > 일반 > AirDrop 및 Handoff > AirPlay 수신 기능을 꺼도 된다.)

### 테스트

```bash
pytest test/
```
