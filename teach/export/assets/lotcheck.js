// Lot-check calculator component, reusable for any produce.
// Markup: <div class="lotcheck"> with inputs carrying data-field="sample" and, per defect,
// a row: <div class="lc-row" data-limit="10"><label>…<input data-field="count"></label><span class="lc-out"></span></div>
// Each row's data-limit is the allowed percentage; editable via an input with data-field="limit" if present.
// Output: percentage of sample and a pass/fail chip, recomputed on every keystroke.
(function () {
  function initLotCheck(box) {
    const sampleInput = box.querySelector('[data-field="sample"]');
    const rows = [...box.querySelectorAll(".lc-row")];
    const verdict = box.querySelector(".lc-verdict");
    function update() {
      const sample = Number(sampleInput.value);
      let allPass = true, anyValid = false;
      rows.forEach((row) => {
        const count = Number(row.querySelector('[data-field="count"]').value);
        const limitInput = row.querySelector('[data-field="limit"]');
        const limit = Number(limitInput ? limitInput.value : row.dataset.limit);
        const out = row.querySelector(".lc-out");
        if (!(sample > 0) || !(count >= 0) || count > sample) { out.textContent = "check numbers"; out.className = "lc-out"; allPass = false; return; }
        anyValid = true;
        const pct = (count / sample) * 100;
        const pass = pct <= limit;
        if (!pass) allPass = false;
        out.textContent = `${pct.toFixed(1)}% vs ${limit}% · ${pass ? "pass" : "fail"}`;
        out.className = "lc-out " + (pass ? "pass" : "fail");
      });
      if (verdict) {
        verdict.textContent = !anyValid ? "Enter the sample size and counts." :
          allPass ? "Lot passes every check entered." : "Lot fails at least one check. Photograph it and tell the buyer before loading.";
        verdict.className = "lc-verdict " + (anyValid ? (allPass ? "pass" : "fail") : "");
      }
    }
    box.addEventListener("input", update);
    update();
  }
  document.querySelectorAll(".lotcheck").forEach(initLotCheck);
})();
