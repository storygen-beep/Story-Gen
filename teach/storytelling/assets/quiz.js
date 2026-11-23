/* Reusable quiz widget.
   Usage in a lesson:
     <div class="quiz" data-quiz-id="0001"></div>
     <script type="application/json" id="quiz-0001">[{ "q": "...", "options": ["a","b","c","d"], "answer": 2, "why": "..." }]</script>
     <script src="../assets/quiz.js"></script>
   Feedback is immediate on click. Only the first click per question counts
   toward the score, so retrying cannot inflate it (retrieval, not guessing). */
(function () {
  const STYLE = `
    .quiz .qcard{margin:1.6rem 0;padding:1rem 1.2rem;background:var(--card);border-radius:4px}
    .quiz .qtext{margin:0 0 .7rem}
    .quiz button.opt{display:block;width:100%;text-align:left;font:inherit;font-size:.95rem;
      background:var(--bg);color:var(--ink);border:1px solid var(--rule);border-radius:3px;
      padding:.55rem .8rem;margin:.35rem 0;cursor:pointer}
    .quiz button.opt:hover{border-color:var(--accent)}
    .quiz button.opt.right{border-color:var(--good);color:var(--good)}
    .quiz button.opt.wrong{border-color:var(--bad);color:var(--bad);text-decoration:line-through}
    .quiz .why{font-size:.9rem;margin:.6rem 0 0;display:none}
    .quiz .why.show{display:block}
    .quiz .score{font-family:var(--sans);font-size:.8rem;color:var(--muted)}`;
  const styleEl = document.createElement("style");
  styleEl.textContent = STYLE;
  document.head.appendChild(styleEl);

  document.querySelectorAll(".quiz[data-quiz-id]").forEach((root) => {
    const id = root.dataset.quizId;
    const dataEl = document.getElementById("quiz-" + id);
    if (!dataEl) return;
    const questions = JSON.parse(dataEl.textContent);
    let firstTryCorrect = 0, answered = 0;
    const score = document.createElement("p");
    score.className = "score";

    questions.forEach((item, qi) => {
      const card = document.createElement("div");
      card.className = "qcard";
      card.innerHTML = `<p class="qtext"><strong>${qi + 1}.</strong> ${item.q}</p>`;
      const why = document.createElement("p");
      why.className = "why";
      let done = false;
      item.options.forEach((label, oi) => {
        const b = document.createElement("button");
        b.className = "opt";
        b.type = "button";
        b.textContent = label;
        b.addEventListener("click", () => {
          const correct = oi === item.answer;
          b.classList.add(correct ? "right" : "wrong");
          if (!done) {
            done = true; answered++;
            if (correct) firstTryCorrect++;
            score.textContent = `First-try score: ${firstTryCorrect} / ${answered} of ${questions.length}`;
          }
          if (correct) { why.innerHTML = item.why; why.classList.add("show"); }
        });
        card.appendChild(b);
      });
      card.appendChild(why);
      root.appendChild(card);
    });
    root.appendChild(score);
  });
})();
