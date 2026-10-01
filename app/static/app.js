const STORAGE_KEY = "service-lab-progress-v2";
const LEGACY_KEY = "service-lab-progress-v1";
const THEME_KEY = "service-lab-theme";
const $ = id => document.getElementById(id);
let questions = [], categories = [], store, state;
let storageAvailable = true;
const pending = new Set();
function applyTheme(theme, persist = false) {
  const isDark = theme === "dark";
  document.documentElement.dataset.theme = isDark ? "dark" : "light";
  const toggle = $("theme-toggle");
  toggle.setAttribute("aria-pressed", String(isDark));
  toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
  toggle.querySelector(".theme-icon").textContent = isDark ? "☀" : "☾";
  toggle.querySelector(".theme-label").textContent = isDark ? "Light mode" : "Dark mode";
  if (persist) {
    try { localStorage.setItem(THEME_KEY, isDark ? "dark" : "light"); } catch (_) {}
  }
}
applyTheme(document.documentElement.dataset.theme === "dark" ? "dark" : "light");
$("theme-toggle").addEventListener("click", () => {
  applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark", true);
});
function baseOrderFor(track) {
  return questions.filter(q => track === "mixed" || q.category === track).map(q => q.id);
}
function freshState(track = store?.activeTrack || "thinking") {
  return {version: 2, order: baseOrderFor(track), mode: "main", index: 0, results: {},
    reviewOrder: [], reviewIndex: 0, reviewResults: {}, reviewHistory: {},
    selections: {}, drafts: {}, hints: {}, practice: {}};
}
function isRecord(v) { return v !== null && typeof v === "object" && !Array.isArray(v); }
function normalizeTrack(saved, track) {
  const s = {...freshState(track), ...(isRecord(saved) ? saved : {})};
  const allowed = new Set(baseOrderFor(track));
  const prior = Array.isArray(s.order) ? s.order : [...allowed];
  const index = Number.isInteger(s.index) ? Math.max(0, s.index) : 0;
  s.order = [...new Set(prior.filter(id => allowed.has(id)))];
  s.index = prior.slice(0, index).filter(id => allowed.has(id)).length;
  for (const id of allowed) if (!s.order.includes(id)) s.order.push(id);
  s.index = Math.min(s.index, s.order.length);
  for (const key of ["results", "reviewResults", "reviewHistory", "selections", "drafts", "hints", "practice"]) {
    if (!isRecord(s[key])) s[key] = {};
  }
  s.reviewOrder = Array.isArray(s.reviewOrder) ? [...new Set(s.reviewOrder.filter(id => allowed.has(id)))] : [];
  s.reviewIndex = Number.isInteger(s.reviewIndex) ? Math.max(0, Math.min(s.reviewIndex, s.reviewOrder.length)) : 0;
  s.mode = s.mode === "review" && s.reviewOrder.length ? "review" : "main";
  return s;
}
function readSaved(key) {
  try { return JSON.parse(localStorage.getItem(key)); } catch (_) { return null; }
}
function loadStore() {
  const saved = readSaved(STORAGE_KEY);
  const result = {version: 2, activeTrack: "thinking", tracks: {}};
  const tracks = ["mixed", ...categories.map(c => c.id)];
  if (saved?.version === 2 && isRecord(saved.tracks)) {
    result.activeTrack = tracks.includes(saved.activeTrack) ? saved.activeTrack : "thinking";
    for (const track of tracks) {
      if (isRecord(saved.tracks[track])) result.tracks[track] = normalizeTrack(saved.tracks[track], track);
    }
  } else {
    const old = readSaved(LEGACY_KEY);
    if (old?.version === 1 && isRecord(old.results)) {
      result.tracks.mixed = normalizeTrack({...old, order: baseOrderFor("mixed"), reviewHistory: old.reviewResults || {}}, "mixed");
      result.activeTrack = "mixed";
    }
  }
  result.tracks[result.activeTrack] ||= freshState(result.activeTrack);
  return result;
}
function saveState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(store)); storageAvailable = true; }
  catch (_) { storageAvailable = false; }
}
function currentOrder() { return state.mode === "review" ? state.reviewOrder : state.order; }
function currentIndex() { return state.mode === "review" ? state.reviewIndex : state.index; }
function currentResults() { return state.mode === "review" ? state.reviewResults : state.results; }
function currentQuestion() { return questions.find(q => q.id === currentOrder()[currentIndex()]); }
function questionKey(id) { return state.mode + ":" + id; }
function pendingKey(id) { return store.activeTrack + ":" + questionKey(id); }
function show(id, visible) { $(id).classList.toggle("hidden", !visible); }
function text(id, value) { $(id).textContent = value ?? ""; }
function trackInfo() {
  return categories.find(c => c.id === store.activeTrack) ||
    {title: "Mixed practice", description: "All 70 questions: 49 multiple choice and 21 coding exercises. Topic sets have different mixes."};
}
function complete(r) { return Boolean(r?.feedback); }
function wrong(r) { return complete(r) && (r.feedback.kind === "choice" ? !r.feedback.correct : !r.selfCorrect); }
function unresolvedIds() {
  return state.order.filter(id => state.practice[id] ?? wrong(complete(state.reviewHistory[id]) ? state.reviewHistory[id] : state.results[id]));
}
function chooseTrack(id) {
  if (id !== "mixed" && !categories.some(c => c.id === id)) return;
  store.activeTrack = id;
  store.tracks[id] ||= freshState(id);
  state = store.tracks[id];
  saveState(); render();
}
function startReview(ids) {
  if (!ids.length) return;
  state.mode = "review"; state.reviewOrder = [...ids]; state.reviewIndex = 0; state.reviewResults = {};
  for (const field of ["drafts", "selections", "hints"]) {
    for (const key of Object.keys(state[field])) if (key.startsWith("review:")) delete state[field][key];
  }
  saveState(); render();
}
function renderFocus() {
  show("focus", true);
  const tabs = $("topic-tabs");
  tabs.replaceChildren();
  categories.forEach((c, i) => {
    const b = document.createElement("button");
    const selected = store.activeTrack === c.id;
    b.type = "button"; b.id = "tab-" + c.id; b.dataset.track = c.id;
    b.setAttribute("role", "tab"); b.setAttribute("aria-selected", String(selected));
    b.setAttribute("aria-controls", "study-panel");
    b.tabIndex = selected || (store.activeTrack === "mixed" && i === 0) ? 0 : -1;
    b.textContent = c.title;
    b.addEventListener("click", () => { chooseTrack(c.id); $("tab-" + c.id).focus(); });
    b.addEventListener("keydown", e => {
      if (!["ArrowRight", "ArrowLeft", "Home", "End"].includes(e.key)) return;
      e.preventDefault();
      const n = e.key === "Home" ? 0 : e.key === "End" ? categories.length - 1 :
        (i + (e.key === "ArrowRight" ? 1 : -1) + categories.length) % categories.length;
      chooseTrack(categories[n].id); $("tab-" + categories[n].id).focus();
    });
    tabs.append(b);
  });
  const info = trackInfo();
  text("focus-title", info.title); text("focus-description", info.description);
  $("mixed-button").setAttribute("aria-pressed", String(store.activeTrack === "mixed"));
  const count = state.order.filter(id => complete(state.results[id])).length;
  const coding = state.order.filter(id => questions.find(q => q.id === id).kind === "code").length;
  text("track-progress", count + " / " + state.order.length + " explored · " + coding + " coding exercise" + (coding === 1 ? "" : "s"));
  const ids = unresolvedIds();
  text("review-button", state.mode === "review" ? "Back to topic" : "Practice again (" + ids.length + ")");
  $("review-button").disabled = state.mode !== "review" && !ids.length;
  const panel = $("study-panel");
  if (store.activeTrack === "mixed") {
    panel.setAttribute("role", "region"); panel.setAttribute("aria-label", info.title); panel.removeAttribute("aria-labelledby");
  } else {
    panel.setAttribute("role", "tabpanel"); panel.setAttribute("aria-labelledby", "tab-" + store.activeTrack); panel.removeAttribute("aria-label");
  }
  show("storage-warning", !storageAvailable);
}
$("mixed-button").addEventListener("click", () => chooseTrack("mixed"));
$("review-button").addEventListener("click", () => {
  if (state.mode === "review") { state.mode = "main"; saveState(); render(); }
  else startReview(unresolvedIds());
});

function render() {
  show("loading", false);
  show("error", false);
  document.body.classList.add("in-progress");
  renderFocus();
  const question = currentQuestion();
  if (!question) {
    show("quiz", false);
    show("summary", true);
    renderSummary();
    return;
  }
  show("summary", false);
  show("quiz", true);
  $("quiz").classList.toggle("code-mode", question.kind === "code");
  const order = currentOrder();
  const number = currentIndex() + 1;
  text("set-label", state.mode === "review" ? "ANOTHER LOOK" : trackInfo().title.toUpperCase());
  text("question-count", `${number} / ${order.length}`);
  const percent = Math.round((currentIndex() / order.length) * 100);
  $("progress-fill").style.width = `${percent}%`;
  $("progress-fill").parentElement.setAttribute("aria-valuenow", String(percent));
  text("kind-badge", question.kind === "choice" ? "Multiple choice" : question.language + " practice");
  text("topic-label", question.topic);
  text("question-title", question.prompt);
  text("question-example", question.example);
  show("question-example", Boolean(question.example));
  show("code-note", question.kind === "code");
  text("validation-message", "");

  const result = currentResults()[question.id];
  renderAnswer(question, result);
  renderHints(question);
  renderFeedback(question, result);
  const isReady = question.kind === "choice" ? state.selections[questionKey(question.id)] !== undefined : Boolean(state.drafts[questionKey(question.id)]?.trim());
  $("submit-button").disabled = Boolean(result) || !isReady || pending.has(pendingKey(question.id));
  text("submit-button", question.kind === "choice" ? "Explore my answer →" : "Guide me through a solution →");
  show("submit-button", !result);
}

function renderAnswer(question, result) {
  const area = $("answer-area");
  area.replaceChildren();
  const key = questionKey(question.id);
  if (question.kind === "choice") {
    const choices = document.createElement("div");
    choices.className = "choices";
    question.options.forEach((option, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "choice";
      button.setAttribute("aria-pressed", String(state.selections[key] === index));
      if (state.selections[key] === index) button.classList.add("selected");
      if (result && (result.feedback.correct || result.revealed) && index === result.feedback.correct_index) button.classList.add("correct");
      if (result && index === result.selected && !result.feedback.correct) button.classList.add("incorrect");
      button.disabled = Boolean(result);
      const letter = document.createElement("span");
      letter.className = "choice-letter";
      letter.textContent = String.fromCharCode(65 + index);
      const label = document.createElement("span");
      label.textContent = option;
      button.append(letter, label);
      button.addEventListener("click", () => {
        state.selections[key] = index;
        saveState();
        render();
      });
      choices.append(button);
    });
    area.append(choices);
  } else {
    const input = document.createElement("textarea");
    input.className = "code-input";
    input.id = "code-answer";
    input.setAttribute("aria-label", `Your ${question.language} answer`);
    input.setAttribute("spellcheck", "false");
    input.value = state.drafts[key] ?? question.starter;
    input.disabled = Boolean(result);
    input.addEventListener("input", () => {
      state.drafts[key] = input.value;
      saveState();
      $("submit-button").disabled = !input.value.trim();
    });
    area.append(input);
  }
}

function renderHints(question) {
  const count = Math.min(state.hints[questionKey(question.id)] || 0, question.hints.length);
  const area = $("hint-area");
  area.replaceChildren();
  question.hints.slice(0, count).forEach((hint, index) => {
    const p = document.createElement("p");
    p.className = "hint";
    p.textContent = `Hint ${index + 1}: ${hint}`;
    area.append(p);
  });
  text("hint-count", count ? `${count} of ${question.hints.length} shown` : "");
  $("hint-button").disabled = count >= question.hints.length;
  text("hint-button", count ? (count >= question.hints.length ? "All hints shown" : "Show another hint ↗") : "Show a hint ↗");
}

function renderFeedback(question, result) {
  show("feedback-card", Boolean(result));
  if (!result) return;
  const feedback = result.feedback;
  const isChoice = question.kind === "choice";
  const source = $("source-link");
  source.replaceChildren();
  show("source-link", Boolean(feedback.source?.startsWith("https://")));
  if (feedback.source?.startsWith("https://")) {
    const link = document.createElement("a");
    link.href = feedback.source; link.target = "_blank"; link.rel = "noopener noreferrer";
    link.textContent = "Read the source ↗"; source.append(link);
  }
  const revealed = !isChoice || feedback.correct || result.revealed;
  text("feedback-kicker", isChoice ? "LET'S LEARN FROM THIS" : "GUIDED WALKTHROUGH");
  text("feedback-title", isChoice ? (feedback.correct ? "That reasoning fits." : "Not quite yet. Take your time.") : "Let's walk through an approach.");
  text("feedback-main", isChoice ? (revealed ? feedback.explanation : "You can try again as often as you like. Ask for another hint, or open the explanation when you're ready.") : "Your code has not been run or automatically checked. Compare the steps and reasoning; different solutions can work too.");
  text("feedback-wrong", isChoice && !feedback.correct && revealed ? feedback.wrong : "");
  show("source-link", revealed && Boolean(feedback.source?.startsWith("https://")));
  show("explain-button", isChoice && !revealed);
  show("code-feedback", !isChoice);
  text("retry-button", isChoice ? "Try this question again" : "Revise my code");
  const practicing = state.practice[question.id] ?? wrong(result);
  $("mark-correct").setAttribute("aria-pressed", String(state.practice[question.id] === false));
  $("mark-review").setAttribute("aria-pressed", String(practicing));
  text("reflection-note", practicing ? "Saved for another look. You can keep trying now or come back later." : state.practice[question.id] === false ? "Understanding noted. You can revisit this topic anytime." : "How does the idea feel? You can keep practicing even after finding the answer.");
  const diagram = $("diagram");
  diagram.replaceChildren();
  if (isChoice && revealed && feedback.diagram) {
    feedback.diagram.forEach((step, index) => {
      if (index) { const arrow = document.createElement("span"); arrow.className = "flow-arrow"; arrow.textContent = "→"; diagram.append(arrow); }
      const item = document.createElement("span"); item.className = "flow-step"; item.textContent = step; diagram.append(item);
    });
    show("diagram", true);
  } else show("diagram", false);
  if (!isChoice) {
    text("reference-code", feedback.reference);
    text("syntax-text", feedback.syntax);
    text("service-text", feedback.service);
    text("pitfall-text", feedback.pitfall);
    const guide = feedback.guide;
    const steps = $("guide-steps");
    steps.replaceChildren();
    (guide?.steps || []).forEach(step => {
      const item = document.createElement("li");
      item.textContent = step;
      steps.append(item);
    });
    text("guide-trace", guide?.trace);
    text("guide-practice", guide?.practice);
    text("guide-practice-answer", guide?.practice_answer);
    show("coding-guide", Boolean(guide));
  }
  show("next-button", true);
  text("next-button", currentIndex() === currentOrder().length - 1 ? "Finish this topic →" : "Continue when ready →");
}

function renderSummary() {
  const reviewing = state.mode === "review";
  const order = reviewing ? state.reviewOrder : state.order;
  const results = reviewing ? state.reviewResults : state.results;
  const missedIds = unresolvedIds().filter(id => !reviewing || order.includes(id));
  const summary = $("summary");
  summary.replaceChildren();
  const add = (tag, content, className) => {
    const element = document.createElement(tag);
    element.textContent = content;
    if (className) element.className = className;
    summary.append(element);
    return element;
  };
  add("p", trackInfo().title.toUpperCase() + (reviewing ? " · REVIEW COMPLETE" : " · SET COMPLETE"), "eyebrow");
  add("h2", "You've spent time learning.");
  add("p", "Take a moment to explain one idea in your own words. You can revisit anything that feels uncertain, repeat the topic, or choose a different focus. There are no scores or limits on attempts.");
  add("h3", missedIds.length ? "Ideas for another look" : "Where would you like to go next?");
  if (missedIds.length) {
    const list = document.createElement("ul"); list.className = "review-list";
    [...new Set(missedIds.map(id => questions.find(q => q.id === id).topic))].forEach(topic => {
      const item = document.createElement("li"); item.textContent = topic; list.append(item);
    });
    summary.append(list);
  }
  const actions = document.createElement("div"); actions.className = "summary-actions";
  if (missedIds.length) {
    const practice = document.createElement("button"); practice.className = "primary-button"; practice.type = "button";
    practice.textContent = "Revisit these ideas →";
    practice.addEventListener("click", () => {
      startReview(missedIds); window.scrollTo(0, 0);
    });
    actions.append(practice);
  }
  if (reviewing) {
    const back = document.createElement("button"); back.className = "secondary-button"; back.type = "button";
    back.textContent = state.index < state.order.length ? "Return to topic" : "Return to topic overview";
    back.addEventListener("click", () => { state.mode = "main"; saveState(); render(); });
    actions.append(back);
  }
  const restart = document.createElement("button"); restart.className = "secondary-button"; restart.type = "button"; restart.textContent = "Explore this topic again";
  restart.addEventListener("click", () => startReview(state.order));
  actions.append(restart); summary.append(actions);
}

function resetProgress() {
  if (!window.confirm("Restart " + trackInfo().title + "? Other topics keep their progress.")) return;
  state = freshState(store.activeTrack);
  store.tracks[store.activeTrack] = state;
  saveState(); render(); window.scrollTo(0, 0);
}

$("reset-button").addEventListener("click", resetProgress);

$("hint-button").addEventListener("click", () => {
  const question = currentQuestion();
  const key = questionKey(question.id);
  state.hints[key] = Math.min((state.hints[key] || 0) + 1, question.hints.length);
  saveState(); renderHints(question);
});

$("submit-button").addEventListener("click", async () => {
  const question = currentQuestion();
  if (!question) return;
  const key = questionKey(question.id), requestKey = pendingKey(question.id);
  if (pending.has(requestKey) || currentResults()[question.id]) return;
  const selected = state.selections[key];
  if (question.kind === "choice" && selected === undefined) { text("validation-message", "Choose the option you want to explore. A guess is a starting point."); return; }
  if (question.kind === "code" && !$("code-answer").value.trim()) { text("validation-message", "Start with any part of your idea, or use a hint to begin."); return; }
  if (question.kind === "code") { state.drafts[key] = $("code-answer").value; saveState(); }
  const targetState = state, targetTrack = store.activeTrack, targetMode = state.mode, targetResults = currentResults();
  const stillHere = () => state === targetState && state.mode === targetMode && currentQuestion()?.id === question.id;
  pending.add(requestKey); $("submit-button").disabled = true; text("validation-message", "");
  try {
    const body = question.kind === "choice" ? {question_id: question.id, selected_index: selected} : {question_id: question.id};
    const response = await fetch("/api/answers", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
    if (!response.ok) throw new Error("The server returned " + response.status + ".");
    const feedback = await response.json();
    if (store.tracks[targetTrack] !== targetState || (targetMode === "review" && targetState.reviewResults !== targetResults)) return;
    const result = {selected: question.kind === "choice" ? selected : null, feedback, selfCorrect: question.kind === "code" ? null : undefined};
    targetResults[question.id] = result;
    targetState.practice[question.id] = Boolean(targetState.practice[question.id] || (question.kind === "choice" ? !feedback.correct : true));
    if (targetMode === "review") targetState.reviewHistory[question.id] = result;
    saveState();
    if (stillHere()) { render(); $("feedback-card").scrollIntoView({behavior: "smooth", block: "nearest"}); }
  } catch (error) {
    if (stillHere()) {
      text("validation-message", "Could not check this answer. " + error.message + " Try again.");
      $("submit-button").disabled = false;
    }
  } finally { pending.delete(requestKey); }
});

function reflect(understood) {
  const question = currentQuestion();
  if (!question || !currentResults()[question.id]) return;
  state.practice[question.id] = !understood;
  saveState(); render();
}
$("mark-correct").addEventListener("click", () => reflect(true));
$("mark-review").addEventListener("click", () => reflect(false));
$("explain-button").addEventListener("click", () => {
  const result = currentResults()[currentQuestion()?.id];
  if (!result) return;
  result.revealed = true;
  saveState(); render();
});
$("retry-button").addEventListener("click", () => {
  const question = currentQuestion();
  if (!question || pending.has(pendingKey(question.id))) return;
  const key = questionKey(question.id);
  delete currentResults()[question.id];
  if (question.kind === "choice") delete state.selections[key];
  saveState(); render();
  if (question.kind === "code") $("code-answer").focus();
  $("question-title").scrollIntoView({behavior: "smooth", block: "start"});
});
$("next-button").addEventListener("click", () => {
  const question = currentQuestion();
  if (!question || !complete(currentResults()[question.id])) return;
  if (state.mode === "review") state.reviewIndex++;
  else state.index++;
  saveState(); render(); window.scrollTo(0, 0);
});

async function start() {
  try {
    const response = await fetch("/api/questions");
    if (!response.ok) throw new Error(`The server returned ${response.status}.`);
    const data = await response.json();
    questions = data.questions;
    if (!questions.length) throw new Error("No questions are available.");
    categories = data.categories;
    store = loadStore();
    state = store.tracks[store.activeTrack];
    saveState();
    render();
  } catch (error) {
    show("loading", false); show("error", true);
    text("error", `Could not load the quiz. ${error.message} Refresh after checking the server.`);
  }
}
start();
