const form = document.getElementById("search-form");
const queryInput = document.getElementById("query");
const suggestionsEl = document.getElementById("suggestions");
const resultSection = document.getElementById("result");
const errorEl = document.getElementById("error");

let selectedTrackId = null;
let activeSuggestionIndex = -1;
let debounceTimer = null;

function debounce(fn, delay) {
  return (...args) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => fn(...args), delay);
  };
}

async function fetchSuggestions(query) {
  const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) return [];
  const data = await response.json();
  return data.results || [];
}

function renderSuggestions(results) {
  suggestionsEl.innerHTML = "";
  activeSuggestionIndex = -1;

  if (results.length === 0) {
    suggestionsEl.hidden = true;
    return;
  }

  results.forEach((track) => {
    const li = document.createElement("li");

    const img = document.createElement("img");
    img.src = track.album_cover || "";
    img.alt = "";

    const span = document.createElement("span");
    span.textContent = `${track.title} - ${track.artist}`;

    li.append(img, span);
    li.addEventListener("click", () => selectSuggestion(track));
    suggestionsEl.appendChild(li);
  });

  suggestionsEl.hidden = false;
}

function selectSuggestion(track) {
  selectedTrackId = track.id;
  queryInput.value = `${track.title} - ${track.artist}`;
  suggestionsEl.hidden = true;
  analyze({ track_id: track.id });
}

const handleInput = debounce(async () => {
  const value = queryInput.value.trim();
  selectedTrackId = null;
  if (value.length < 2) {
    suggestionsEl.hidden = true;
    return;
  }
  renderSuggestions(await fetchSuggestions(value));
}, 300);

queryInput.addEventListener("input", handleInput);

queryInput.addEventListener("keydown", (event) => {
  const items = Array.from(suggestionsEl.children);
  if (suggestionsEl.hidden || items.length === 0) return;

  if (event.key === "ArrowDown") {
    event.preventDefault();
    activeSuggestionIndex = (activeSuggestionIndex + 1) % items.length;
  } else if (event.key === "ArrowUp") {
    event.preventDefault();
    activeSuggestionIndex = (activeSuggestionIndex - 1 + items.length) % items.length;
  } else if (event.key === "Escape") {
    suggestionsEl.hidden = true;
    return;
  } else if (event.key === "Enter" && activeSuggestionIndex >= 0) {
    event.preventDefault();
    items[activeSuggestionIndex].click();
    return;
  } else {
    return;
  }

  items.forEach((item, index) => item.classList.toggle("active", index === activeSuggestionIndex));
});

document.addEventListener("click", (event) => {
  if (!form.contains(event.target)) {
    suggestionsEl.hidden = true;
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();
  if (!query) return;
  suggestionsEl.hidden = true;
  analyze(selectedTrackId ? { track_id: selectedTrackId } : { query });
});

async function analyze(body) {
  errorEl.hidden = true;
  resultSection.hidden = true;

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "분석에 실패했습니다.");
    }

    document.getElementById("result-cover").src = data.track.album_cover || "";
    document.getElementById("result-title").textContent = `${data.track.title} - ${data.track.artist}`;
    document.getElementById("result-mood").textContent = `${data.mood.mood_ko} (${data.mood.mood_en})`;
    document.getElementById("result-bpm").textContent = data.track.bpm
      ? `${Math.round(data.track.bpm)}${data.track.bpm_estimated ? " (추정)" : ""}`
      : "정보 없음";
    document.getElementById("result-lyrics").textContent = data.lyrics_used
      ? "사용함"
      : "사용 안 함 (가사를 찾지 못함)";

    resultSection.hidden = false;
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  }
}
