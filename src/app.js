import { quizData } from './data.js';
import { initTouchInteractions } from './touchHandler.js';

const ROUND_SIZE = 5;
let roundOffset = 0;
let currentIdx = 0;
let score = 0;
let answered = false;

export function initApp() {
  initTouchInteractions();
  renderQuestion();
  setupEventListeners();
}

function getCurrentQuestion() {
  return quizData[(roundOffset + currentIdx) % quizData.length];
}

function renderQuestion() {
  answered = false;
  const q = getCurrentQuestion();
  
  const categoryElem = document.getElementById('categoryText');
  const counterElem = document.getElementById('counterText');
  const questionElem = document.getElementById('questionText');
  const progressFill = document.getElementById('progressFill');

  if (categoryElem) categoryElem.textContent = q.category;
  if (counterElem) counterElem.textContent = `${currentIdx + 1} / ${ROUND_SIZE} (전체 ${quizData.length}문항 중 #${((roundOffset + currentIdx) % quizData.length) + 1})`;
  if (questionElem) questionElem.textContent = q.question;
  if (progressFill) progressFill.style.width = `${((currentIdx + 1) / ROUND_SIZE) * 100}%`;
  
  const expBox = document.getElementById('explanationBox');
  const nextBtn = document.getElementById('nextBtn');
  if (expBox) expBox.className = 'explanation-box';
  if (nextBtn) nextBtn.className = 'next-btn';

  const grid = document.getElementById('optionsGrid');
  if (grid) {
    grid.innerHTML = '';
    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.setAttribute('type', 'button');
      btn.setAttribute('aria-label', `선택지 ${idx + 1}: ${opt}`);
      btn.textContent = opt;
      btn.onclick = () => selectOption(idx);
      grid.appendChild(btn);
    });
  }
}

function selectOption(selectedIdx) {
  if (answered) return;
  answered = true;

  const q = getCurrentQuestion();
  const buttons = document.querySelectorAll('.option-btn');
  const isCorrect = (selectedIdx === q.answer);

  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    if (idx === q.answer) {
      btn.classList.add('correct');
    } else if (idx === selectedIdx) {
      btn.classList.add('wrong');
    }
  });

  if (isCorrect) score++;

  const expBox = document.getElementById('explanationBox');
  const expResult = document.getElementById('expResult');
  const expText = document.getElementById('expText');
  
  if (expResult) {
    expResult.textContent = isCorrect ? "✅ 정답" : "❌ 오답";
    expResult.style.color = isCorrect ? "var(--correct)" : "var(--wrong)";
  }
  if (expText) expText.textContent = `${q.explanation} [출처: ${q.source}]`;
  if (expBox) expBox.classList.add('show');

  const nextBtn = document.getElementById('nextBtn');
  if (nextBtn) {
    nextBtn.textContent = (currentIdx === ROUND_SIZE - 1) ? "결과 보기" : "다음 문제로";
    nextBtn.classList.add('show');
    setTimeout(() => {
      try {
        nextBtn.focus();
      } catch (e) {}
    }, 200);
  }
}

export function nextQuestion() {
  if (currentIdx < ROUND_SIZE - 1) {
    currentIdx++;
    renderQuestion();
  } else {
    showResults();
  }
}

function showResults() {
  const quizCard = document.getElementById('quizCard');
  const resultCard = document.getElementById('resultCard');
  if (quizCard) quizCard.style.display = 'none';
  if (resultCard) resultCard.classList.add('show');

  const finalScoreElem = document.getElementById('finalScore');
  if (finalScoreElem) finalScoreElem.textContent = score;
  
  const rankTitle = document.getElementById('rankTitle');
  const rankDesc = document.getElementById('rankDesc');

  if (score === 5) {
    if (rankTitle) rankTitle.textContent = "🏆 0.1% 상식 브레인 마스터!";
    if (rankDesc) rankDesc.textContent = "5문항을 모두 완벽하게 맞추셨습니다. 상식 내공이 대단합니다!";
  } else if (score >= 3) {
    if (rankTitle) rankTitle.textContent = "🥈 스마트한 상식 탐험가!";
    if (rankDesc) rankDesc.textContent = "뛰어난 상식 감각을 가지고 계십니다. 다음 5문항 세트도 도전해보세요!";
  } else {
    if (rankTitle) rankTitle.textContent = "🥉 상식 호기심 가득한 루키!";
    if (rankDesc) rankDesc.textContent = "새로운 지식을 채우는 재미를 느껴보세요. 다음 세트도 도전!";
  }
}

export function restartQuiz() {
  currentIdx = 0;
  score = 0;
  answered = false;
  const resultCard = document.getElementById('resultCard');
  const quizCard = document.getElementById('quizCard');
  if (resultCard) resultCard.classList.remove('show');
  if (quizCard) quizCard.style.display = 'block';
  renderQuestion();
}

export function nextRoundSet() {
  roundOffset = (roundOffset + ROUND_SIZE) % quizData.length;
  restartQuiz();
  showToast(`다음 5문항 세트(#${roundOffset + 1}~#${roundOffset + ROUND_SIZE})가 시작됩니다!`);
}

export async function shareResult() {
  const rankTitleElem = document.getElementById('rankTitle');
  const rank = rankTitleElem ? rankTitleElem.textContent : "상식 퀴즈 도전자";
  const shareText = `[notopened 상식 퀴즈] 5문제 중 ${score}문제를 맞췄습니다!\n나의 등급: ${rank}\n지금 바로 도전해보세요! #notopened #상식퀴즈`;
  
  if (navigator.share) {
    try {
      await navigator.share({
        title: 'notopened 1일 1상식 두뇌 퀴즈',
        text: shareText,
        url: window.location.href
      });
      showToast("공유되었습니다!");
      return;
    } catch (err) {
      if (err.name === 'AbortError') return;
    }
  }

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(shareText).then(() => {
      showToast("결과가 클립보드에 복사되었습니다!");
    }).catch(() => {
      fallbackCopyText(shareText);
    });
  } else {
    fallbackCopyText(shareText);
  }
}

function fallbackCopyText(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  try {
    document.execCommand('copy');
    showToast("결과가 클립보드에 복사되었습니다!");
  } catch (err) {
    showToast("클립보드 복사 권한이 필요합니다.");
  }
  document.body.removeChild(textArea);
}

export function showToast(msg) {
  const toast = document.getElementById('toast');
  if (toast) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(() => toast.classList.remove('show'), 2500);
  }
}

function handleGamePromo(e) {
  const btn = e.target.closest('.game-link-btn');
  if (!btn) return;
  const gameId = btn.getAttribute('data-game');
  if (gameId === '001') {
    showToast("GAME #001 (린샤오 | 손끝의 순발력과 두뇌 회전이 만나는 1분 상식 서바이벌) 출시 준비 중!");
  } else if (gameId === '002') {
    showToast("GAME #002 (노아 | 하루 5분, 어휘력과 추리력을 깨우는 감성 워드 퍼즐) 출시 준비 중!");
  } else if (gameId === '003') {
    showToast("GAME #003 (루카 | 양자 매듭 두뇌 힐링 라인 퍼즐 Knot Flow v1.2.2) QA 통과 완료!");
  } else {
    showToast("패밀리 게임 출시 준비 중입니다.");
  }
}

function setupEventListeners() {
  const nextBtn = document.getElementById('nextBtn');
  if (nextBtn) nextBtn.addEventListener('click', nextQuestion);

  const restartBtn = document.getElementById('restartBtn');
  if (restartBtn) restartBtn.addEventListener('click', restartQuiz);

  const nextSetBtn = document.getElementById('nextSetBtn');
  if (nextSetBtn) nextSetBtn.addEventListener('click', nextRoundSet);

  const shareBtn = document.getElementById('shareBtn');
  if (shareBtn) shareBtn.addEventListener('click', shareResult);

  const crossPromo = document.querySelector('.cross-promo');
  if (crossPromo) {
    crossPromo.addEventListener('click', handleGamePromo);
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', initApp);
  window.nextQuestion = nextQuestion;
  window.restartQuiz = restartQuiz;
  window.nextRoundSet = nextRoundSet;
  window.shareResult = shareResult;
  window.showToast = showToast;
}
