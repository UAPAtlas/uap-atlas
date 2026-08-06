/* UAP Atlas · Blackfile analytical mode controller */
(() => {
  'use strict';
  if (typeof blackfileAnalysis === 'undefined' || !Array.isArray(blackfileAnalysis.questions)) {
    console.error('Blackfile analysis payload unavailable.');
    return;
  }

  const questions = blackfileAnalysis.questions;
  const questionIds = new Set(questions.map(q => q.id));
  const body = document.body;
  const shell = document.getElementById('blackfileShell');
  const toggle = document.getElementById('blackfileModeToggle');
  const modeLabel = document.getElementById('blackfileModeLabel');
  const brandSecondary = document.querySelector('#atlasHome .brand-secondary');
  const signal = document.getElementById('blackfileSignal');
  const constellation = document.getElementById('blackfileConstellation');
  const brief = document.getElementById('blackfileBrief');
  const evidence = document.getElementById('blackfileEvidence');
  if (!shell || !toggle || !signal || !constellation || !brief || !evidence) {
    console.error('Blackfile mode shell is incomplete.');
    return;
  }

  const bfEsc = value => String(value ?? '').replace(/[&<>\"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[ch]));
  const modeIsBlackfile = () => state.appMode === 'blackfile';
  const selectedQuestion = () => questions.find(q => q.id === state.selectedQuestionId) || questions[0];
  const caseById = id => cases.find(c => c.id === id);
  const toneSignal = { strong:'84%', documented:'90%', mixed:'58%', weak:'24%' };

  state.appMode = 'atlas';
  state.selectedQuestionId = questions[0].id;

  function signalMarkup() {
    return questions.map(q => `
      <button class="bf-signal-node ${q.id === state.selectedQuestionId ? 'active' : ''}" type="button" data-bf-question="${bfEsc(q.id)}" data-tone="${bfEsc(q.tone)}" aria-pressed="${q.id === state.selectedQuestionId}" style="--signal:${toneSignal[q.tone] || '50%'}">
        <span class="q">Q${String(q.number).padStart(2, '0')}</span>
        <strong>${bfEsc(q.railTitle || q.shortTitle)}</strong><i aria-hidden="true"></i>
      </button>`).join('');
  }

  function constellationMarkup() {
    const positions = {q1:[50,10],q2:[79,27],q3:[79,70],q4:[50,88],q5:[21,70],q6:[21,27]};
    const lines = Object.entries(positions).map(([, [x,y]]) => `<line x1="50" y1="49" x2="${x}" y2="${y}"></line>`).join('');
    const nodes = questions.map(q => `
      <button class="bf-question-node ${q.id === state.selectedQuestionId ? 'active' : ''}" type="button" data-bf-question="${bfEsc(q.id)}" data-question="${bfEsc(q.id)}" data-tone="${bfEsc(q.tone)}" aria-pressed="${q.id === state.selectedQuestionId}" aria-label="Question ${q.number}: ${bfEsc(q.title)}">
        <span class="node-top"><span class="node-q">Q${String(q.number).padStart(2, '0')}</span><i class="node-dot" aria-hidden="true"></i></span>
        <strong>${bfEsc(q.shortTitle)}</strong><small>${bfEsc(q.status)}</small>
      </button>`).join('');
    return `<div class="bf-orbit" aria-hidden="true"></div><svg class="bf-link-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">${lines}<circle cx="50" cy="49" r="1.1"></circle></svg>${nodes}<div class="bf-core-caption">Evidence registry → analytical synthesis</div>`;
  }

  function listMarkup(items) {
    return items.map(item => `<li>${bfEsc(item)}</li>`).join('');
  }

  function supplementalMarkup(q) {
    const briefs = Array.isArray(q.supplementalAnalysis) ? q.supplementalAnalysis : [];
    if (!briefs.length) return '';
    return briefs.map(item => {
      const findings = listMarkup(item.findings || []);
      const boundaries = listMarkup(item.boundaries || []);
      const sources = (item.sources || []).map(source => `<li><a href="${bfEsc(source.url)}" target="_blank" rel="noopener noreferrer">${bfEsc(source.label)}</a><small>${bfEsc(source.role)}</small></li>`).join('');
      return `<section class="bf-brief-section bf-supplemental-analysis">
        <div class="bf-brief-context"><span class="bf-number">Supplemental Blackfile · Analysis only</span><span class="bf-confidence">${bfEsc(item.classification)}</span></div>
        <h3>${bfEsc(item.title)}</h3>
        <span class="bf-status" data-tone="weak">${bfEsc(item.status)}</span>
        <p>${bfEsc(item.summary)}</p>
        <h4>What the source record establishes</h4><ul>${findings}</ul>
        <h4>Interpretive boundaries</h4><ul>${boundaries}</ul>
        <h4>Source ledger</h4><ul class="bf-supplemental-sources">${sources}</ul>
      </section>`;
    }).join('');
  }

  function briefMarkup(q) {
    const tensions = q.tensions.map(t => `<div class="bf-tension"><b>${bfEsc(t.label)}</b><p>${bfEsc(t.summary)}</p></div>`).join('');
    return `
      <div class="bf-brief-context"><span class="bf-number">Question ${String(q.number).padStart(2,'0')} · State of Evidence</span><span class="bf-confidence">${bfEsc(q.confidence)}</span></div>
      <h2 class="bf-brief-title">${bfEsc(q.title)}</h2>
      <span class="bf-status" data-tone="${bfEsc(q.tone)}">${bfEsc(q.status)}</span>
      <div class="bf-answer"><b>Current answer</b><p>${bfEsc(q.answer)}</p></div>
      ${supplementalMarkup(q)}
      <section class="bf-brief-section"><h3>What the evidence supports</h3><ul>${listMarkup(q.findings)}</ul></section>
      <section class="bf-brief-section counter"><h3>Competing evidence & calibration</h3><ul>${listMarkup(q.counterEvidence)}</ul></section>
      <section class="bf-brief-section"><h3>D10 contradiction boundaries</h3>${tensions}</section>
      <section class="bf-brief-section missing"><h3>Evidence that would change the answer</h3><ul>${listMarkup(q.missingEvidence)}</ul></section>
      <div class="bf-brief-foot">Analysis layer · ${bfEsc(blackfileAnalysis.analysisSource)}<br>Boundary ledger · ${bfEsc(blackfileAnalysis.boundarySource)}</div>`;
  }

  function evidenceMarkup(q) {
    const linked = q.caseIds.map(caseById).filter(Boolean);
    const rows = linked.map(c => `
      <button class="bf-case-row" type="button" data-bf-case="${bfEsc(c.id)}" aria-label="Open Atlas dossier for ${bfEsc(c.title)}">
        <span class="case-id">${bfEsc(c.id)}</span><span class="case-copy"><strong>${bfEsc(c.title)}</strong><small>${bfEsc(c.date)} · ${bfEsc(c.agency)}</small></span><span class="arrow" aria-hidden="true">→</span>
      </button>`).join('');
    return `<div class="bf-evidence-head"><div><strong>Evidence Stack</strong><span>${bfEsc(q.shortTitle)} · existing Atlas records</span></div><div class="bf-evidence-count">${linked.length} linked case${linked.length === 1 ? '' : 's'}</div></div><div class="bf-evidence-list">${rows}</div>`;
  }

  function bindRenderedControls() {
    document.querySelectorAll('[data-bf-question]').forEach(btn => btn.addEventListener('click', () => {
      const openBrief = Boolean(btn.closest('.bf-constellation-stage')) && isMobileAtlas();
      selectBlackfileQuestion(btn.dataset.bfQuestion, {openBrief});
    }));
    document.querySelectorAll('[data-bf-case]').forEach(btn => btn.addEventListener('click', () => openLinkedCase(btn.dataset.bfCase)));
  }

  function renderBlackfile() {
    const q = selectedQuestion();
    signal.innerHTML = signalMarkup();
    constellation.innerHTML = constellationMarkup();
    brief.innerHTML = briefMarkup(q);
    evidence.innerHTML = evidenceMarkup(q);
    bindRenderedControls();
  }

  function syncMobileLabels() {
    document.querySelectorAll('.mobile-nav [data-page]').forEach(btn => {
      const label = btn.querySelector('.mobile-nav-label');
      const text = modeIsBlackfile() ? label?.dataset.blackfile : label?.dataset.atlas;
      if (label && text) label.textContent = text;
      if (text) btn.setAttribute('aria-label', text);
      if (btn.classList.contains('active')) btn.setAttribute('aria-current', 'page');
      else btn.removeAttribute('aria-current');
    });
    const landscapeLabel = document.querySelector('[data-landscape-exit] span');
    if (landscapeLabel) landscapeLabel.textContent = modeIsBlackfile() ? 'Evidence' : 'Cases';
  }

  function syncModeChrome() {
    const blackfile = modeIsBlackfile();
    body.dataset.atlasMode = blackfile ? 'blackfile' : 'atlas';
    shell.hidden = !blackfile;
    toggle.setAttribute('aria-pressed', String(blackfile));
    toggle.setAttribute('aria-label', blackfile ? 'Return to UAP Case Atlas' : 'Open Blackfile analytical mode');
    if (modeLabel) modeLabel.textContent = blackfile ? 'Atlas' : 'Blackfile';
    if (brandSecondary) brandSecondary.textContent = blackfile ? 'UAP Blackfile' : 'UAP Case Atlas';
    syncMobileLabels();
  }

  function setBlackfileMobilePage(page, {write=true} = {}) {
    mobilePage = mobilePages.has(page) ? page : 'map';
    document.getElementById('drawerBackdrop')?.classList.remove('open');
    urlCaseId = null;
    syncMobileNav();
    if (write) updateUrl();
  }

  function setAtlasMode(mode, {write=true} = {}) {
    const next = mode === 'blackfile' ? 'blackfile' : 'atlas';
    if (next === 'blackfile') {
      state.appMode = 'blackfile';
      document.getElementById('drawerBackdrop')?.classList.remove('open');
      urlCaseId = null;
      if (isMobileAtlas()) mobilePage = 'map';
      renderBlackfile();
    } else {
      state.appMode = 'atlas';
      if (isMobileAtlas() && mobilePage === 'dossier' && !document.getElementById('drawerBackdrop')?.classList.contains('open')) mobilePage = 'map';
    }
    syncModeChrome();
    syncMobileNav();
    if (write) updateUrl();
  }

  function selectBlackfileQuestion(id, {openBrief=false, write=true} = {}) {
    if (!questionIds.has(id)) return;
    state.selectedQuestionId = id;
    renderBlackfile();
    if (openBrief && isMobileAtlas()) setBlackfileMobilePage('dossier', {write});
    else if (write) updateUrl();
  }

  function openLinkedCase(id) {
    const c = caseById(id);
    if (!c) return;
    if (isMobileAtlas()) {
      /* Preserve the Blackfile Evidence state as the browser-Back destination. */
      try { history.pushState({atlasReturn:'blackfile-evidence'}, '', location.pathname + location.search + location.hash); }
      catch (_) {}
      setAtlasMode('atlas', {write:false});
      selectCase(id, true);
      setMobilePage('dossier');
      return;
    }
    selectCase(id, false);
    openFullCase(id);
  }

  /* Preserve all established URL state, then add the analytical mode keys. */
  const atlasUpdateUrl = updateUrl;
  updateUrl = function() {
    atlasUpdateUrl();
    const params = new URLSearchParams(location.hash.replace(/^#\/?/, ''));
    if (modeIsBlackfile()) {
      params.set('mode', 'blackfile');
      params.set('question', state.selectedQuestionId);
      params.delete('case');
    } else {
      params.delete('mode');
      params.delete('question');
    }
    const query = params.toString();
    lastWrittenHash = query ? `#${query}` : '';
    try { history.replaceState(null, '', location.pathname + location.search + lastWrittenHash); }
    catch (_) { location.hash = lastWrittenHash; }
  };

  /* Let the established mobile controller own Atlas pages; intercept only in Blackfile. */
  const atlasSyncMobileNav = syncMobileNav;
  syncMobileNav = function() {
    atlasSyncMobileNav();
    syncMobileLabels();
  };
  document.querySelectorAll('.mobile-nav [data-page]').forEach(btn => btn.addEventListener('click', event => {
    if (!modeIsBlackfile()) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    setBlackfileMobilePage(btn.dataset.page);
  }, true));

  toggle.addEventListener('click', () => setAtlasMode(modeIsBlackfile() ? 'atlas' : 'blackfile'));
  document.getElementById('atlasHome')?.addEventListener('click', () => {
    if (modeIsBlackfile()) setAtlasMode('atlas', {write:false});
  }, true);

  /* Stop hidden Atlas keyboard navigation and use arrows to explore questions. */
  document.addEventListener('keydown', event => {
    if (!modeIsBlackfile() || !['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(event.key)) return;
    const tag = (event.target.tagName || '').toLowerCase();
    if (['input','select','textarea'].includes(tag)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    const index = Math.max(0, questions.findIndex(q => q.id === state.selectedQuestionId));
    const delta = event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? -1 : 1;
    selectBlackfileQuestion(questions[(index + delta + questions.length) % questions.length].id);
  }, true);

  function syncFromLocation(useInitial=false) {
    const sourceHash = useInitial && window.__blackfileInitialHash ? window.__blackfileInitialHash : location.hash;
    if (useInitial) window.__blackfileInitialHash = null;
    const params = new URLSearchParams(sourceHash.replace(/^#\/?/, ''));
    const q = params.get('question');
    if (q && questionIds.has(q)) state.selectedQuestionId = q;
    state.appMode = params.get('mode') === 'blackfile' ? 'blackfile' : 'atlas';
    if (isMobileAtlas() && mobilePages.has(params.get('page'))) mobilePage = params.get('page');
    if (modeIsBlackfile()) {
      document.getElementById('drawerBackdrop')?.classList.remove('open');
      urlCaseId = null;
    }
    syncModeChrome();
    if (modeIsBlackfile()) renderBlackfile();
  }
  window.addEventListener('popstate', () => syncFromLocation(false));
  window.addEventListener('hashchange', () => syncFromLocation(false), true);

  syncFromLocation(true);
  renderBlackfile();
  syncMobileNav();
  if (modeIsBlackfile()) updateUrl();
  window.blackfileMode = {setMode:setAtlasMode, selectQuestion:selectBlackfileQuestion, render:renderBlackfile};
})();
