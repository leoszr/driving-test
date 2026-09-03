const QUESTION_COUNT = 50;
const PASSING_SCORE = 40;
const STORAGE_KEY = "nj-drive-prep-results";

const screens = {
  start: document.querySelector("#start-screen"),
  quiz: document.querySelector("#quiz-screen"),
  result: document.querySelector("#result-screen"),
  error: document.querySelector("#error-screen"),
};

const elements = {
  start: document.querySelector("#start-button"),
  clear: document.querySelector("#clear-history"),
  emptyHistory: document.querySelector("#empty-history"),
  historyContent: document.querySelector("#history-content"),
  historyList: document.querySelector("#history-list"),
  bestScore: document.querySelector("#best-score"),
  lastScore: document.querySelector("#last-score"),
  progressLabel: document.querySelector("#progress-label"),
  progressBar: document.querySelector("#progress-bar"),
  liveScore: document.querySelector("#live-score"),
  questionNumber: document.querySelector("#question-number"),
  questionTitle: document.querySelector("#question-title"),
  questionImage: document.querySelector("#question-image"),
  options: document.querySelector("#options"),
  feedback: document.querySelector("#feedback"),
  next: document.querySelector("#next-button"),
  resultBadge: document.querySelector("#result-badge"),
  resultTitle: document.querySelector("#result-title"),
  resultCopy: document.querySelector("#result-copy"),
  finalScore: document.querySelector("#final-score"),
  retry: document.querySelector("#retry-button"),
  home: document.querySelector("#home-button"),
};

let questionBank = [];
let questions = [];
let current = 0;
let score = 0;
let answered = false;

function showScreen(name) {
  Object.entries(screens).forEach(([key, screen]) => { screen.hidden = key !== name; });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index--) {
    const random = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[random]] = [copy[random], copy[index]];
  }
  return copy;
}

function getHistory() {
  try {
    const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    return Array.isArray(value) ? value : [];
  } catch {
    return [];
  }
}

function saveResult(result) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify([result, ...getHistory()].slice(0, 10)));
}

function renderHistory() {
  const history = getHistory();
  const hasHistory = history.length > 0;
  elements.emptyHistory.hidden = hasHistory;
  elements.historyContent.hidden = !hasHistory;
  elements.clear.hidden = !hasHistory;
  if (!hasHistory) return;

  elements.bestScore.textContent = `${Math.max(...history.map(item => item.score))}/50`;
  elements.lastScore.textContent = `${history[0].score}/50`;
  elements.historyList.replaceChildren(...history.slice(0, 5).map(item => {
    const row = document.createElement("li");
    const date = document.createElement("time");
    date.dateTime = item.date;
    date.textContent = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(new Date(item.date));
    const grade = document.createElement("strong");
    grade.textContent = `${item.score}/50 · ${item.score >= PASSING_SCORE ? "Aprovado" : "Reprovado"}`;
    row.append(date, grade);
    return row;
  }));
}

function startQuiz() {
  questions = shuffle(questionBank).slice(0, QUESTION_COUNT);
  current = 0;
  score = 0;
  showScreen("quiz");
  renderQuestion();
}

function renderQuestion() {
  answered = false;
  const question = questions[current];
  const displayNumber = current + 1;

  elements.progressLabel.textContent = `Questão ${displayNumber} de ${QUESTION_COUNT}`;
  elements.progressBar.style.width = `${displayNumber / QUESTION_COUNT * 100}%`;
  elements.liveScore.textContent = `${score} ${score === 1 ? "acerto" : "acertos"}`;
  elements.questionNumber.textContent = `Questão ${displayNumber}`;
  elements.questionTitle.textContent = question.question;
  elements.feedback.hidden = true;
  elements.feedback.className = "feedback";
  elements.next.hidden = true;
  elements.next.textContent = displayNumber === QUESTION_COUNT ? "Ver resultado" : "Próxima questão";

  if (question.image) {
    elements.questionImage.src = question.image;
    elements.questionImage.hidden = false;
  } else {
    elements.questionImage.removeAttribute("src");
    elements.questionImage.hidden = true;
  }

  const labels = question.options.map((option, index) => {
    const label = document.createElement("label");
    label.className = "option";
    const input = document.createElement("input");
    input.type = "radio";
    input.name = "answer";
    input.value = index;
    input.addEventListener("change", () => answerQuestion(index));
    const key = document.createElement("span");
    key.className = "option-key";
    key.textContent = String.fromCharCode(65 + index);
    const text = document.createElement("span");
    text.className = "option-text";
    text.textContent = option;
    label.append(input, key, text);
    return label;
  });
  elements.options.replaceChildren(...labels);
  elements.questionTitle.focus({ preventScroll: true });
}

function answerQuestion(selected) {
  if (answered) return;
  answered = true;
  const question = questions[current];
  const correct = selected === question.answer;
  if (correct) score++;

  [...elements.options.children].forEach((label, index) => {
    label.classList.add("locked");
    label.querySelector("input").disabled = true;
    if (index === question.answer) label.classList.add("correct");
    if (index === selected && !correct) label.classList.add("incorrect");
  });

  elements.liveScore.textContent = `${score} ${score === 1 ? "acerto" : "acertos"}`;
  elements.feedback.classList.add(correct ? "correct" : "incorrect");
  elements.feedback.innerHTML = correct
    ? "<strong>Resposta correta.</strong> Continue assim."
    : `<strong>Resposta incorreta.</strong> A alternativa correta é <b>${String.fromCharCode(65 + question.answer)}</b>: ${escapeHtml(question.options[question.answer])}`;
  elements.feedback.hidden = false;
  elements.next.hidden = false;
  elements.next.focus({ preventScroll: true });
}

function escapeHtml(value) {
  const node = document.createElement("span");
  node.textContent = value;
  return node.innerHTML;
}

function nextQuestion() {
  if (!answered) return;
  current++;
  if (current < QUESTION_COUNT) renderQuestion();
  else finishQuiz();
}

function finishQuiz() {
  const passed = score >= PASSING_SCORE;
  saveResult({ score, date: new Date().toISOString() });
  elements.resultBadge.textContent = passed ? "✓" : "×";
  elements.resultTitle.textContent = passed ? "Você atingiu a meta." : "Ainda não foi desta vez.";
  elements.resultCopy.textContent = passed
    ? `Você acertou ${score} de 50 questões e alcançou os 80% exigidos no teste de conhecimentos.`
    : `Você acertou ${score} de 50 questões. Revise o conteúdo e tente novamente — a meta é 40 acertos.`;
  elements.finalScore.textContent = score;
  showScreen("result");
}

function goHome() {
  renderHistory();
  showScreen("start");
}

elements.start.addEventListener("click", startQuiz);
elements.retry.addEventListener("click", startQuiz);
elements.home.addEventListener("click", goHome);
elements.next.addEventListener("click", nextQuestion);
elements.clear.addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  renderHistory();
});

fetch("questions.json")
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(data => {
    if (!Array.isArray(data) || data.length < QUESTION_COUNT) throw new Error("Banco insuficiente");
    questionBank = data;
    renderHistory();
  })
  .catch(() => showScreen("error"));
