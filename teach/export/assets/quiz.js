// Quiz component, shared by every lesson.
// Markup: <div class="quiz"> <div class="q" data-answer="2"> <p class="prompt">…</p>
//   <div class="opts"><button>…</button>…</div> <p class="why" hidden>…</p> </div> … <p class="score"></p></div>
// data-answer is the 0-based index of the correct button. First click locks the question,
// marks right/wrong, and reveals the explanation, so feedback is immediate.
(function () {
  function initQuiz(quiz) {
    const questions = [...quiz.querySelectorAll(".q")];
    const score = quiz.querySelector(".score");
    let answered = 0, correct = 0;
    const render = () => { if (score) score.textContent = `${correct} / ${answered} correct · ${questions.length - answered} left`; };
    questions.forEach((q) => {
      const answer = Number(q.dataset.answer);
      const buttons = [...q.querySelectorAll(".opts button")];
      buttons.forEach((btn, i) => {
        btn.type = "button";
        btn.addEventListener("click", () => {
          buttons.forEach((b) => (b.disabled = true));
          buttons[answer].classList.add("right");
          if (i !== answer) btn.classList.add("wrong"); else correct++;
          answered++;
          const why = q.querySelector(".why");
          if (why) why.hidden = false;
          render();
        });
      });
    });
    render();
  }
  document.querySelectorAll(".quiz").forEach(initQuiz);
})();
