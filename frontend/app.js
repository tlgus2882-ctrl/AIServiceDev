const form = document.getElementById("search-form");
const resultSection = document.getElementById("result");
const errorEl = document.getElementById("error");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = document.getElementById("query").value.trim();
  if (!query) return;

  errorEl.hidden = true;
  resultSection.hidden = true;

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "분석에 실패했습니다.");
    }

    document.getElementById("result-title").textContent = `${data.track.title} - ${data.track.artist}`;
    document.getElementById("result-mood").textContent = `${data.mood.mood_ko} (${data.mood.mood_en})`;
    document.getElementById("result-bpm").textContent = data.track.bpm ? Math.round(data.track.bpm) : "정보 없음";
    document.getElementById("result-lyrics").textContent = data.lyrics_used ? "사용함" : "사용 안 함 (가사를 찾지 못함)";

    resultSection.hidden = false;
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  }
});
