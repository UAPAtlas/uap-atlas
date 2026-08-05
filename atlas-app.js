/* UAP Atlas application runtime. Loaded with defer after atlas-runtime.js. */
const labels = [
  {name:'North America', x:18, y:11},{name:'South America', x:24, y:48},{name:'Europe', x:50, y:14},{name:'Africa', x:51, y:33},{name:'Asia', x:76, y:17},{name:'Australia', x:88, y:45},{name:'Antarctica', x:50, y:59}
];
const state = { selectedCaseId: null, selectedEventId: null, stackMode:'main', zoom: 1, view: {x:0, y:0, w:100, h:62}, pan: {x:0, y:0}, dragging:false, dragStart:null, filters:{agency:'all', domain:'all', precision:'all', q:'', era:'all'}, institutional:true };
const cases = atlasData.cases.slice().sort((a,b)=>a.year-b.year || a.id.localeCompare(b.id));
const events = atlasData.timeline.slice().sort((a,b)=>a.year-b.year || a.id.localeCompare(b.id));
const svg = document.getElementById('atlasSvg');
const caseGeometryG = document.getElementById('caseGeometry');
const markersG = document.getElementById('markers');
const selectionLayer = document.getElementById('selectionLayer');
const clustersG = document.getElementById('clusters');
const labelsG = document.getElementById('labels');
const stateLinesG = document.getElementById('stateLines');
const detail = document.getElementById('detail');
const caseList = document.getElementById('caseList');
const timeline = document.getElementById('signalCanvas');
const corpusLayer = document.getElementById('corpusLayer');
const nodeLayer = document.getElementById('nodeLayer');
const decadeTicks = document.getElementById('decadeTicks');
const signalWrap = document.getElementById('signalWrap');
const signalTooltip = document.getElementById('signalTooltip');
const caseCount = document.getElementById('caseCount');
const stackTitle = document.getElementById('stackTitle');
const stackSubtitle = document.getElementById('stackSubtitle');
const stackReturn = document.getElementById('stackReturn');
const agencyFilter = document.getElementById('agencyFilter');
const domainFilter = document.getElementById('domainFilter');
const precisionFilter = document.getElementById('precisionFilter');
const toggleInstitutional = document.getElementById('toggleInstitutional');
const colorByMode = { exact:'marker-exact', unresolved:'marker-unresolved', redacted:'marker-redacted', orbital:'marker-orbital', institutional:'marker-institutional' };
const statusPill = { exact:'cyan', unresolved:'amber', redacted:'violet', orbital:'white', institutional:'silver' };
function clamp(v,min,max){return Math.max(min,Math.min(max,v));}
function currentZoom(){return 100 / state.view.w;}
function markerScale(){return clamp(1/state.zoom,0.22,1);}
function selectionBeaconScale(){return markerScale()*(window.matchMedia('(max-width:1080px)').matches?1.28:1);}
function selectedMarkerScale(){return markerScale()*1.85;}
function setView(x,y,w){
  state.view={x,y,w,h:w*0.62};
  svg.setAttribute('viewBox',`${x} ${y} ${w} ${w*0.62}`);
  state.zoom=currentZoom();
  const zr=document.getElementById('zoomReadout');
  if(zr) zr.textContent=`${state.zoom.toFixed(1)}×`;
  if(stateLinesG){
    const alpha=clamp(0.28 + (state.zoom-1)*0.075, 0.28, 0.72);
    stateLinesG.style.setProperty('--state-line-alpha', alpha.toFixed(3));
  }
  const ms=markerScale();
  document.querySelectorAll('.atlas-marker').forEach(el=>{
    const mx=el.dataset.x, my=el.dataset.y;
    const sc=el.classList.contains('selected')&&!el.classList.contains('orbital-aggregate')?selectedMarkerScale():ms;
    if(mx&&my) el.setAttribute('transform',`translate(${mx},${my}) scale(${sc})`);
  });
  document.querySelectorAll('.cluster-badge').forEach(el=>{
    const mx=el.dataset.x, my=el.dataset.y;
    if(mx&&my) el.setAttribute('transform',`translate(${mx},${my}) scale(${ms})`);
  });
  renderClusters();
  updateSelectionBeaconTransform();
}
let viewAnim=null, viewAnimGuard=null;
function cancelViewAnim(){
  if(viewAnim){cancelAnimationFrame(viewAnim); viewAnim=null;}
  if(viewAnimGuard){clearTimeout(viewAnimGuard); viewAnimGuard=null;}
}
function animateView(x,y,w,dur=460){
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){setView(x,y,w); return;}
  cancelViewAnim();
  const from={...state.view}; const t0=performance.now();
  const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
  const step=now=>{
    const p=Math.min(1,(now-t0)/dur), e=ease(p);
    setView(from.x+(x-from.x)*e, from.y+(y-from.y)*e, from.w+(w-from.w)*e);
    if(p<1){viewAnim=requestAnimationFrame(step);}
    else{viewAnim=null; if(viewAnimGuard){clearTimeout(viewAnimGuard); viewAnimGuard=null;}}
  };
  viewAnim=requestAnimationFrame(step);
  // if rAF is throttled or suspended, still land on the target view
  viewAnimGuard=setTimeout(()=>{if(viewAnim!==null){cancelViewAnim(); setView(x,y,w);}},dur+150);
}
function zoomToCase(x,y,level=6.25){const w=100/level, h=w*0.62; animateView(clamp(x-w/2,0,100-w), clamp(y-h/2,0,62-h), w);}
function resetView(){animateView(0,0,100);}
function markerStatus(c){return c.mode==='exact'?'exact':c.mode==='unresolved'?'unresolved':c.mode==='redacted'?'redacted':c.mode==='orbital'?'orbital':'institutional';}
function isOrbitalCase(c){return markerStatus(c)==='orbital';}
function stackModeForCase(c){return isOrbitalCase(c)?'orbital':'main';}
function stackBaseCases(){return state.stackMode==='orbital'?cases.filter(isOrbitalCase):cases.filter(c=>!isOrbitalCase(c));}
function visibleStackCases(){return stackBaseCases().filter(matchesFilters);}
function syncStackHeader(){
  const mainCases=cases.filter(c=>!isOrbitalCase(c));
  const mainCounted=mainCases.filter(c=>c.countInCaseTotals!==false).length;
  const seriesIndexes=mainCases.filter(c=>c.recordRole==='series-parent').length;
  const orbitalTotal=cases.filter(isOrbitalCase).length;
  if(stackTitle) stackTitle.textContent=state.stackMode==='orbital'?'Orbital / Lunar Evidence':'Case Stack';
  if(stackSubtitle) stackSubtitle.textContent=state.stackMode==='orbital'?`${orbitalTotal} NASA release-corpus records`:`${mainCounted} counted incidents${seriesIndexes?` · ${seriesIndexes} series index${seriesIndexes===1?'':'es'}`:''}`;
  if(stackReturn) stackReturn.hidden=state.stackMode!=='orbital';
}
function setStackMode(mode,opts={}){
  state.stackMode=mode==='orbital'?'orbital':'main';
  const list=visibleStackCases();
  const fallback=stackBaseCases()[0]||cases[0]||null;
  if(opts.select!==false && (!state.selectedCaseId || !list.some(c=>c.id===state.selectedCaseId))){state.selectedCaseId=(list[0]||fallback||{}).id||null;}
  if(opts.render!==false){renderAll(); updateUrl();}
}
function resetStackFilters(){
  state.filters={agency:'all',domain:'all',precision:'all',q:'',era:'all'};
  agencyFilter.value='all'; domainFilter.value='all'; precisionFilter.value='all';
  const cs=document.getElementById('caseSearch'); if(cs) cs.value='';
  if(typeof buildEraRail==='function') buildEraRail();
}
function matchesFilters(c){if(state.filters.agency!=='all' && c.agency!==state.filters.agency) return false; if(state.filters.domain!=='all' && !c.domain.includes(state.filters.domain)) return false; if(state.filters.precision!=='all' && markerStatus(c)!==state.filters.precision) return false; if(state.filters.q){const hay=`${c.id} ${c.title} ${c.location} ${c.agency} ${c.date} ${c.domain}`.toLowerCase(); if(!state.filters.q.split(/\s+/).every(t=>hay.includes(t))) return false;} if(state.filters.era!=='all' && Math.floor(c.year/10)*10!==state.filters.era) return false; return true;}
function buildFilters(){const agencies=['all',...new Set(cases.map(c=>c.agency))]; const domains=['all',...new Set(cases.map(c=>c.domain.split(' / ')[0]))]; const precisions=['all','exact','unresolved','redacted','orbital','institutional']; agencyFilter.innerHTML=agencies.map(v=>`<option value="${v}">Agency: ${v==='all'?'All':v}</option>`).join(''); domainFilter.innerHTML=domains.map(v=>`<option value="${v}">Domain: ${v==='all'?'All':v}</option>`).join(''); precisionFilter.innerHTML=precisions.map(v=>`<option value="${v}">Precision: ${v==='all'?'All':v}</option>`).join('');}
function renderLabels(){labelsG.innerHTML = labels.map(l=>`<text class="label" x="${l.x}" y="${l.y}">${l.name}</text>`).join('');}
function caseCard(c){const active = c.id===state.selectedCaseId ? 'active' : ''; const status=markerStatus(c); return `<div class="case-row ${active}" data-id="${c.id}" role="button" tabindex="0" aria-label="Select ${esc(c.title)}, ${esc(c.date)}"><div class="file-id"><div class="id">${c.id}</div><small>${c.date}</small></div><div class="file-main"><div class="t">${c.title}</div><div class="m">${c.location} · ${c.agency}</div></div><div class="row-actions"><div class="pill ${statusPill[status]}">${c.mode}</div></div></div>`;}
function renderCaseList(){const base=stackBaseCases(); const filtered = base.filter(matchesFilters); syncStackHeader(); caseCount.textContent = `${filtered.length} / ${base.length}`; const empty=state.stackMode==='orbital'?'No orbital / lunar evidence matches the current filters.':'No main-stack cases match the current filters.'; caseList.innerHTML = filtered.map(caseCard).join('') || `<div class="empty">${empty}</div>`; caseList.querySelectorAll('.case-row').forEach(el=>{const choose=()=>selectCase(el.dataset.id,true);el.addEventListener('click',choose);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose();}});});}
function quoteHtml(c,caption=true){if(!c.keyQuote) return ''; const source=caption&&c.quoteSource?`<figcaption>${esc(c.quoteSource)} · ${esc(c.quoteConfidence||'quote selected')}</figcaption>`:''; return `<figure class="quote-card"><blockquote>“${esc(c.keyQuote)}”</blockquote>${source}</figure>`;}
function keyFactHtml(c,includeWhy=false){const hero=includeWhy; const quote=hero?quoteHtml(c,false):''; const meta=hero?factMetaLine(c):''; const why=hero&&c.whyItMatters?`<div class="why-card"><b>Why it matters</b><p>${esc(c.whyItMatters)}</p></div>`:''; return `<div class="case-intel ${hero?'fact-hero':''}"><div class="label2">Key finding</div><div class="key-fact-copy">${esc(c.heroFact||c.keyFact||c.summary)}</div>${quote}${meta}</div>${why}`;}
function renderDetail(){const c = cases.find(x=>x.id===state.selectedCaseId); if(!c){detail.innerHTML = '<div class="empty">Select a case from the map, list, or timeline.</div>'; return;} const files=filesForCase(c).length||evidenceItems(c).length; detail.innerHTML = `<div class="preview-context"><div class="eyebrow">${esc(c.mode)} · ${esc(c.domain)}</div><div class="meta">${esc(c.id)} · ${esc(c.date)}</div></div><div class="case-title">${esc(c.title)}</div><div class="loc">${esc(c.location)} · ${esc(c.agency)}</div>${c.mapGeometry?`<div class="geometry-context">Map overlay · ${esc(c.mapGeometry.isObjectTrack?'object track':(['LineString','MultiLineString'].includes(c.mapGeometry.type)?'reference route':'approximate area'))} · ${esc(c.mapGeometry.confidence||'approximate')}</div>`:''}${c.image?`<button class="detail-media" type="button" data-open-case="${esc(c.id)}" aria-label="Open dossier evidence"><img src="${esc(c.image)}" alt="" loading="lazy"><span class="detail-media-tag">Evidence · ${esc(String(files))} file${files===1?'':'s'}</span></button>`:''}${keyFactHtml(c,false)}${c.summary?`<div class="preview-summary"><b>Summary</b><p>${esc(c.summary)}</p></div>`:''}<div class="preview-meta-line"><span><b>Source</b>${esc(c.sourceLabel||c.agency)}</span><span><b>Files</b>${esc(String(files))}</span><span><b>Date</b>${esc(c.date)}</span></div><button class="cta" type="button" data-open-case="${esc(c.id)}">Open Dossier <span aria-hidden="true">→</span></button>`; detail.querySelectorAll('[data-open-case]').forEach(btn=>btn.addEventListener('click',()=>openFullCase(btn.dataset.openCase)));}
function typeClass(t){return t==='official-position'?'official-position':t;}
/* Normalize 10 raw event types into 7 visual color buckets */
function signalTypeClass(t){
  if(t==='incident'||t==='case') return 't-case';
  if(t==='investigation') return 't-investigation';
  if(t==='official-position') return 't-official-position';
  if(t==='contradiction') return 't-contradiction';
  if(t==='release') return 't-release';
  if(t==='orbital') return 't-orbital';
  return 't-other';
}
/* Position an event on the horizontal axis as a percentage of the full year range */
function eventX(ev){
  const minY=events[0].year, maxY=events[events.length-1].year;
  const pad=0.018;
  const span=Math.max(1,maxY-minY);
  return pad+(ev.year-minY)/span*(1-2*pad);
}
function renderDecadeTicks(){
  if(!decadeTicks) return;
  const minY=events[0].year, maxY=events[events.length-1].year;
  const firstDec=Math.floor(minY/10)*10;
  const lastDec=Math.floor(maxY/10)*10;
  let html='';
  for(let d=firstDec; d<=lastDec; d+=10){
    const dummy={year:d};
    const x=eventX(dummy);
    const isAnchor=(d===minY);
    html+=`<div class="decade-tick ${isAnchor?'anchor':''}" style="left:${(x*100).toFixed(2)}%"><span class="year">${d}</span></div>`;
  }
  decadeTicks.innerHTML=html;
}
function renderSignal(){
  const visible=events.filter(ev=>state.institutional || ev.type!=='official-position');
  const era=state.filters.era;
  const inEra=ev=>era==='all'||Math.floor(ev.year/10)*10===era;
  renderDecadeTicks();
  if(corpusLayer){
    corpusLayer.innerHTML=visible.map(ev=>{
      const x=eventX(ev)*100;
      return `<div class="corpus-dot ${signalTypeClass(ev.type)} ${inEra(ev)?'':'era-out'}" style="left:${x.toFixed(2)}%" data-case="${esc(ev.caseId)}" data-event="${esc(ev.id)}" data-date="${esc(ev.date)}" data-title="${esc(ev.title)}"></div>`;
    }).join('');
    corpusLayer.querySelectorAll('.corpus-dot').forEach(el=>{
      el.addEventListener('click',()=>{state.selectedEventId=el.dataset.event; selectCase(el.dataset.case,true);});
      el.addEventListener('mouseenter',e=>showSignalTooltip(el));
      el.addEventListener('mouseleave',hideSignalTooltip);
    });
  }
  if(nodeLayer){
    const sel=state.selectedCaseId;
    if(!sel){ nodeLayer.innerHTML=''; }
    else{
      const nodes=visible.filter(ev=>ev.caseId===sel);
      nodeLayer.innerHTML=nodes.map(ev=>{
        const x=eventX(ev)*100;
        return `<div class="signal-node ${signalTypeClass(ev.type)} ${ev.id===state.selectedEventId?'selected':''} ${inEra(ev)?'':'era-out'}" style="left:${x.toFixed(2)}%" data-case="${esc(ev.caseId)}" data-event="${esc(ev.id)}"><div class="node-dot"></div><div class="node-date">${esc(ev.date)}</div></div>`;
      }).join('');
      nodeLayer.querySelectorAll('.signal-node').forEach(el=>{
        el.addEventListener('click',()=>{state.selectedEventId=el.dataset.event; selectCase(el.dataset.case,true);});
      });
    }
  }
  const hdr=document.getElementById('timelineHeader');
  if(hdr){
    if(era==='all'){ hdr.textContent=`${events[0].year}—${events[events.length-1].year} · ${visible.length} EVENTS`; }
    else{ const n=visibleStackCases().length; hdr.textContent=`${era}s · ${n} ${state.stackMode==='orbital'?'ORBITAL ':'CASE'}${n===1?'':'S'} IN VIEW`; }
  }
}
function showSignalTooltip(el){
  if(!signalTooltip) return;
  const rect=el.getBoundingClientRect();
  const wrapRect=signalWrap.getBoundingClientRect();
  signalTooltip.querySelector('.tt-date').textContent=el.dataset.date||'';
  signalTooltip.querySelector('.tt-title').textContent=el.dataset.title||'';
  const x=rect.left-wrapRect.left+rect.width/2;
  const y=rect.top-wrapRect.top;
  signalTooltip.style.left=`${x}px`;
  signalTooltip.style.top=`${y}px`;
  signalTooltip.classList.add('show');
}
function hideSignalTooltip(){ if(signalTooltip) signalTooltip.classList.remove('show'); }
function markerEl(c){
  const cls=colorByMode[markerStatus(c)];
  const selected=c.id===state.selectedCaseId;
  const sc=selected?selectedMarkerScale():markerScale();
  return `<g class="atlas-marker ${cls} ${selected?'selected':''}" data-id="${c.id}" data-x="${c.x}" data-y="${c.y}" transform="translate(${c.x},${c.y}) scale(${sc})"><circle class="marker-halo" r="1.0"/><circle class="marker-ring" r="0.7"/><circle class="marker-core" r="0.4"/></g>`;
}
function orbitalAggregateEl(orbitals){
  if(!orbitals.length) return '';
  const selected=orbitals.some(c=>c.id===state.selectedCaseId) ? 'selected' : '';
  const active=orbitals.find(c=>c.id===state.selectedCaseId) || orbitals[0];
  const count=orbitals.length;
  const x=50, y=7.7;
  return `<g class="atlas-marker orbital-aggregate marker-orbital ${selected}" data-id="${active.id}" data-x="${x}" data-y="${y}" transform="translate(${x},${y}) scale(${markerScale()})"><path class="orbital-arc-glow" d="M -39 2.6 Q 0 -10.8 39 2.6"/><path class="orbital-arc" d="M -39 2.6 Q 0 -10.8 39 2.6"/><circle class="orbital-node-outer" r="1.42"/><circle class="orbital-node-inner" r=".56"/><text class="orbital-count" text-anchor="middle" dominant-baseline="middle">${count}</text><text class="orbital-label" x="3.0" y="-.34">ORBITAL / LUNAR EVIDENCE</text><text class="orbital-caption" x="3.0" y="1.12">NASA RELEASE CORPUS</text></g>`;
}
function renderCaseGeometry(){
  if(!caseGeometryG) return;
  const c=cases.find(x=>x.id===state.selectedCaseId);
  const g=c?.mapGeometry;
  if(!g?.d){caseGeometryG.innerHTML=''; return;}
  const route=g.type==='LineString'||g.type==='MultiLineString';
  const qualifier=g.isObjectTrack?'object track':route?'reference route':'approximate area';
  caseGeometryG.innerHTML=`<g class="case-geometry ${route?'is-route':'is-area'}" data-id="${esc(c.id)}" data-kind="${esc(qualifier)}" aria-label="${esc(`${qualifier}; ${g.confidence||'approximate'}`)}"><path class="case-geometry-shape" d="${esc(g.d)}"/></g>`;
}

function renderMarkers(){
  const visible=cases.filter(matchesFilters);
  const orbitals=visible.filter(c=>markerStatus(c)==='orbital');
  const terrestrial=visible.filter(c=>markerStatus(c)!=='orbital');
  const selectedTerrestrial=terrestrial.filter(c=>c.id===state.selectedCaseId);
  const regularTerrestrial=terrestrial.filter(c=>c.id!==state.selectedCaseId);
  markersG.innerHTML = regularTerrestrial.map(markerEl).join('') + orbitalAggregateEl(orbitals) + selectedTerrestrial.map(markerEl).join('');
  markersG.querySelectorAll('.atlas-marker').forEach(el=>el.addEventListener('click',()=>{
    const c=cases.find(c=>c.id===el.dataset.id);
    if(c && markerStatus(c)==='orbital') return selectOrbitalAggregate(el.dataset.id);
    selectCase(el.dataset.id,true);
  }));
}
function selectOrbitalAggregate(id){
  state.stackMode='orbital';
  resetStackFilters();
  const target=cases.find(c=>c.id===id && isOrbitalCase(c)) || cases.find(isOrbitalCase);
  if(target) state.selectedCaseId=target.id;
  resetView();
  renderAll();
  updateUrl();
  if(target) highlightRow(target.id);
}
function renderClusters(){
  clustersG.innerHTML='';
  const visible=cases.filter(matchesFilters).filter(c=>markerStatus(c)!=='orbital');
  const used=new Set();
  const clusters=[];
  const threshold=3/state.zoom;
  for(let i=0;i<visible.length;i++){
    if(used.has(i)) continue;
    const a=visible[i]; const group=[a]; used.add(i);
    for(let j=i+1;j<visible.length;j++){
      if(used.has(j)) continue;
      const b=visible[j];
      if(Math.hypot(a.x-b.x,a.y-b.y)<=threshold){group.push(b); used.add(j);}
    }
    if(group.length>1) clusters.push(group);
  }
  const ms=markerScale();
  clusters.forEach((g,idx)=>{
    const x=g.reduce((sum,c)=>sum+c.x,0)/g.length;
    const y=g.reduce((sum,c)=>sum+c.y,0)/g.length;
    clustersG.insertAdjacentHTML('beforeend',`<g class="cluster-badge" data-index="${idx}" data-x="${x}" data-y="${y}" transform="translate(${x},${y}) scale(${ms})"><rect class="cluster-pill" x="-1.6" y="-0.95" rx="0.75" ry="0.75" width="3.2" height="1.9"/><text class="cluster-text" text-anchor="middle" dominant-baseline="middle">${g.length}</text></g>`);
  });
  clustersG.querySelectorAll('.cluster-badge').forEach(el=>el.addEventListener('click',()=>{
    const g=clusters[Number(el.dataset.index)];
    const x=g.reduce((sum,c)=>sum+c.x,0)/g.length;
    const y=g.reduce((sum,c)=>sum+c.y,0)/g.length;
    zoomToCase(x,y,6);
  }));
}

function updateSelectionBeaconTransform(){
  if(!selectionLayer) return;
  const beacon=selectionLayer.querySelector('.selection-beacon');
  if(!beacon) return;
  const x=beacon.dataset.x, y=beacon.dataset.y;
  if(x&&y) beacon.setAttribute('transform',`translate(${x},${y}) scale(${selectionBeaconScale()})`);
}
function selectionAnchorCase(){
  const c=cases.find(x=>x.id===state.selectedCaseId);
  if(!c) return null;
  if(!cases.filter(matchesFilters).some(x=>x.id===c.id)) return null;
  return c;
}
function renderSelectionBeacon(pulse=false){
  if(!selectionLayer) return;
  const c=selectionAnchorCase();
  if(!c){selectionLayer.innerHTML=''; return;}
  const above=Number(c.y)>12;
  const labelY=above?-5.35:4.15;
  const lineStart=above?-2.78:2.58;
  const lineEnd=above?-4.02:3.42;
  const w=clamp(String(c.id).length*.48+2.65,5.4,11.8);
  const labelX=-w/2;
  const wave=pulse?'<circle class="selection-wave" r="1.12"/>':'';
  selectionLayer.innerHTML=`<g class="selection-beacon" data-x="${esc(c.x)}" data-y="${esc(c.y)}" transform="translate(${esc(c.x)},${esc(c.y)}) scale(${selectionBeaconScale()})">${wave}<circle class="selection-reticle selection-reticle-outer" r="2.75"/><circle class="selection-reticle selection-reticle-inner" r="1.42"/><circle class="selection-spark" r=".2"/><line class="selection-label-stem" x1="0" y1="${lineStart}" x2="0" y2="${lineEnd}"/><g class="selection-label" transform="translate(${labelX},${labelY})"><rect class="selection-label-bg" x="0" y="0" width="${w}" height="2.35" rx=".56"/><text class="selection-label-kicker" x="${w/2}" y=".78">SELECTED</text><text class="selection-label-id" x="${w/2}" y="1.72">${esc(c.id)}</text></g><path class="selection-bracket" d="M -2.95 -1.55 L -2.95 -2.95 L -1.55 -2.95 M 1.55 -2.95 L 2.95 -2.95 L 2.95 -1.55 M 2.95 1.55 L 2.95 2.95 L 1.55 2.95 M -1.55 2.95 L -2.95 2.95 L -2.95 1.55"/></g>`;
}


function esc(v){return String(v??'').replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));}

const mapShellEl=document.getElementById('mapShell');
const mapTip=document.getElementById('mapTip');
function hideMapTip(){if(mapTip) mapTip.classList.remove('on');}
function moveMapTip(e){
  const r=mapShellEl.getBoundingClientRect();
  let x=e.clientX-r.left+14, y=e.clientY-r.top+12;
  if(x+mapTip.offsetWidth>r.width-10) x=e.clientX-r.left-mapTip.offsetWidth-14;
  if(y+mapTip.offsetHeight>r.height-10) y=e.clientY-r.top-mapTip.offsetHeight-12;
  mapTip.style.transform=`translate(${Math.max(8,x)}px,${Math.max(8,y)}px)`;
}
svg.addEventListener('mousemove',e=>{
  if(!mapTip) return;
  if(state.dragging) return hideMapTip();
  const m=e.target.closest('.atlas-marker,.cluster-badge');
  if(!m) return hideMapTip();
  if(m.classList.contains('cluster-badge')){
    const n=m.querySelector('.cluster-text')?.textContent||'';
    mapTip.innerHTML=`<b>Cluster</b><strong>${esc(n)} linked cases</strong><span>Click to zoom into this cluster</span>`;
  }else if(m.classList.contains('orbital-aggregate')){
    mapTip.innerHTML=`<b>Orbital / lunar evidence</b><strong>NASA release corpus</strong><span>Click to review orbital records</span>`;
  }else{
    const c=cases.find(x=>x.id===m.dataset.id);
    if(!c) return hideMapTip();
    mapTip.innerHTML=`<b>${esc(c.id)}</b><strong>${esc(c.title)}</strong><span>${esc(c.location)} · ${esc(c.date)}</span>`;
  }
  mapTip.classList.add('on');
  moveMapTip(e);
});
svg.addEventListener('mouseleave',hideMapTip);
function drawerTimeline(id){return events.filter(e=>e.caseId===id).map(e=>`<div class="drawer-timeline-row"><b>${esc(e.date)}</b><i></i><div><strong>${esc(e.title)}</strong><span>${esc(e.desc||'Normalized atlas timeline event.')}</span></div></div>`).join('') || '<p class="drawer-summary">No normalized timeline event yet.</p>';}
function linkUrl(path){const s=String(path||''); if(/^https?:\/\//i.test(s)||/^(?:assets\/|\.\/|\.\.\/|data:|blob:)/i.test(s)) return s; if(s.startsWith('/')) return '#local-file-not-published'; return s;}
function fileUrl(path){return linkUrl(path);}
function sourceTokens(src){const s=String(src||'').toUpperCase(); return Object.keys(sourceFileIndex).filter(tok=>s.includes(String(tok).toUpperCase()));}
function mediaKind(path){const raw=String(path||''); if(/^https?:\/\//i.test(raw)) return 'url'; const ext=raw.split('?')[0].split('.').pop().toLowerCase(); if(['jpg','jpeg','png','gif','webp'].includes(ext)) return 'image'; if(['mp4','mov','webm'].includes(ext)) return 'video'; if(ext==='pdf') return 'pdf'; return 'file';}
function fileName(path){return String(path||'').split('/').pop();}
function sourceActionLabel(kind,path=''){if(kind==='video') return 'Watch source video'; if(kind==='image') return 'View archival image'; if(kind==='pdf') return 'Open source document'; if(kind==='url'&&/(?:youtube\.com|youtu\.be|dvidshub\.net\/video)/i.test(path)) return 'Watch external video'; if(kind==='url') return 'View external source'; return 'Open source file';}
function sourceAvailability(path){return sourceAvailabilityIndex.entries[String(path||'')]||{status:'unavailable',label:'Availability not verified'};}
function sourceIsActionable(path){return ['public-local','external-public'].includes(sourceAvailability(path).status);}
function sourceDisclosureHtml(file){
  const availability=sourceAvailability(file.path);
  if(sourceIsActionable(file.path)) return `<a class="file-link" href="${esc(fileUrl(file.path))}" target="_blank" rel="noopener" title="${esc(file.path)}">${esc(sourceActionLabel(file.kind,file.path))}<small>${esc(fileName(file.path))}</small></a>`;
  const custody=availability.status==='custody-only';
  const label=custody?'Research corpus':'Unavailable mapping';
  return `<span class="source-disclosure ${custody?'source-custody':'source-unavailable'}" title="${esc(file.path)}"><span>${label}</span><small>${esc(fileName(file.path))}</small><small>${esc(availability.label)}</small></span>`;
}
function filesForSource(src){
  const out=[]; const seen=new Set();
  sourceTokens(src).forEach(tok=>(sourceFileIndex[tok]||[]).forEach(path=>{if(!seen.has(path)){seen.add(path); out.push({token:tok,path,kind:mediaKind(path),availability:sourceAvailability(path)});}}));
  return out;
}
function filesForCase(c){const out=[]; const seen=new Set(); (c.sources||[]).forEach(src=>filesForSource(src).forEach(f=>{if(!seen.has(f.path)){seen.add(f.path); out.push(f);}})); return out;}
function titleCase(v){return String(v||'').toLowerCase().replace(/\b[a-z]/g,ch=>ch.toUpperCase()).replace(/\bUap\b/g,'UAP').replace(/\bUfo\b/g,'UFO').replace(/\bCia\b/g,'CIA').replace(/\bNasa\b/g,'NASA').replace(/\bFbi\b/g,'FBI').replace(/\bDoe\b/g,'DOE').replace(/\bUsaf\b/g,'USAF').replace(/\bRaf\b/g,'RAF');}
function compactConfidence(v){const s=String(v||'').trim(); if(/^CONFIRMED RECORD$/i.test(s)) return 'Confirmed'; if(/^CONFIRMED QUOTATION$/i.test(s)) return 'Confirmed quote'; if(/^CONFIRMED RELEASE RECORD$/i.test(s)) return 'Confirmed release'; if(/^RELEASED RECORD$/i.test(s)) return 'Released'; return titleCase(s);}
function factMetaLine(c){const parts=[c.significance||'Case significance',c.sourceQuality||'Source record',c.sourceLocator||c.sourceLabel].filter(Boolean); return parts.length?`<div class="fact-meta">${parts.map(esc).join(' · ')}</div>`:'';}
function briefFooterStrip(c){const files=filesForCase(c).length||evidenceItems(c).length; const cells=[['CONFIDENCE',compactConfidence(c.confidence)],['SOURCE',c.sourceLabel||c.agency||'Source record'],['FILES',String(files)],['DATE',c.date]]; return `<div class="dossier-strip">${cells.map(([k,v])=>`<div class="strip-cell"><b>${esc(k)}</b><span>${esc(v)}</span></div>`).join('')}</div>`;}
function relatedRecordsHtml(c){const ids=(c.relatedCaseIds||[]).filter(id=>id!==c.id&&cases.some(x=>x.id===id)).slice(0,3); const links=ids.map(id=>{const r=cases.find(x=>x.id===id); return `<button class="related-chip" type="button" data-related-case="${esc(id)}">${esc(r.title)}</button>`;}).join(''); const ctx=(c.relatedContext||[]).map(label=>`<span class="related-chip">${esc(label)}</span>`).join(''); if(!links&&!ctx) return ''; return `<div class="related-records"><div class="label2">Related records</div><div class="related-scroll">${links}${ctx}</div></div>`;}
function culturalLegacyHtml(c){
  const items=c.culturalLegacy||[]; if(!items.length) return '';
  const rows=items.map(item=>{
    const imageHref=item.imageSourceUrl||item.image;
    const source=item.sourceUrl?`<a href="${esc(linkUrl(item.sourceUrl))}" target="_blank" rel="noopener">Source</a>`:'';
    const rights=item.licenseUrl?`<a href="${esc(linkUrl(item.licenseUrl))}" target="_blank" rel="noopener">${esc(item.license||'License')}</a>`:esc(item.rightsStatus||item.license||'');
    return `<article class="cultural-item"><a class="cultural-image" href="${esc(linkUrl(imageHref))}" target="_blank" rel="noopener"><img src="${esc(item.image)}" alt="${esc(item.imageAlt||item.title)}" loading="lazy" decoding="async"></a><div class="cultural-copy"><h4>${esc(item.title)}${item.year?`<span class="cultural-year">${esc(item.year)}</span>`:''}</h4><p>${esc(item.connection)}</p><div class="cultural-meta"><span>${esc(item.credit||'Context image')}</span>${source}${rights}</div></div></article>`;
  }).join('');
  return `<section class="cultural-legacy" aria-label="Cultural Legacy"><div class="cultural-legacy-head"><div class="cultural-legacy-title">Cultural Legacy</div><div class="cultural-legacy-boundary">Context · Not evidence</div></div>${rows}</section>`;
}
function lensRecords(c){return (c.sourceRecords||[]).filter(r=>!/evidence[- ]?(?:audit|depth)/i.test(`${r.sourceType||''} ${r.locator||''}`)&&!String(r.locator||'').startsWith('source-files/'));}
function lensEvidenceClass(c,records){const official=/official|primary|intelligence|debrief|contract|government|usaf|raf|dia|cia|faa|nasa|cable|military/;const derivative=/public-copy|public-scan|mirror|transcript|press|testimony|witness|archive-index/;const types=records.map(r=>String(r.sourceType||'').toLowerCase()),all=types.join(' '),officialCount=types.filter(t=>official.test(t)&&!derivative.test(t)).length;if(/finding-aid|collection-guide/.test(all)&&records.length===1)return'Institutional locator';if(officialCount===records.length&&records.length>1)return'Multiple official records';if(officialCount&&records.length>1)return'Official + supporting records';if(officialCount===1)return'Primary / official record';if(/contemporaneous.*press|newspaper|wire-service/.test(all))return'Contemporary press';if(/witness|testimony|interview|investigator/.test(all))return'Witness / investigator trail';if(/photo|media|film|tape/.test(all))return'Media / image record';return records.length>1?'Multiple structured records':'Structured source record';}
function lensCustody(c,records){const text=`${c.sourceQuality||''} ${c.quoteConfidence||''}`.toLowerCase(),acquisition=/unrecovered|not publicly recovered|not recovered|no complete sheriff|no complete official|not complete faa|no official investigative packet|complete packet unavailable|complete file unavailable|sheriff\/search packet|no first-party|first-party file unavailable|first-party archive|no authenticated original|original negative|original tape custody|native agency|native media master|native operational packet|primary-page|primary pages not fully mapped|primary law-enforcement pages/;if((c.acquisitionTargets||[]).some(target=>String(target||'').trim())||acquisition.test(text))return{label:'Acquisition required',tone:'partial'};const types=records.map(r=>String(r.sourceType||'')).join(' ').toLowerCase();if(/finding-aid|collection-guide/.test(types)&&!/primary|official|intelligence|government/.test(types))return{label:'Locator only',tone:'locator'};if(records.length)return{label:'Mapped custody',tone:'mapped'};return{label:'Context only',tone:'locator'};}
function lensQuoteSignal(c){const s=String(c.quoteConfidence||'').trim();if(/^high\b/i.test(s))return'High';if(/^medium[- ]?high\b/i.test(s))return'Medium-high';if(/^medium\b/i.test(s))return'Medium';if(/^low[- ]?medium\b/i.test(s))return'Low-medium';if(/confirmed|verified/i.test(s))return'Verified';if(/web article|summary/i.test(s))return'Contextual';return s.split(/[—.;]/)[0]||'Unrated';}
function orbitalEvidenceLabel(value){return String(value||'').replaceAll('-',' ').replace(/\b\w/g,m=>m.toUpperCase());}
function orbitalEvidenceLensHtml(c){
  const e=c.orbitalEvidence; if(!e) return '';
  const supports=(e.supports||[]).slice(0,3);
  const unresolved=[...(e.doesNotEstablish||[]).slice(0,1),...(e.limitations||[]).slice(0,2)];
  const list=items=>items.map(x=>`<li>${esc(x)}</li>`).join('');
  return `<section class="evidence-lens orbital-evidence-lens" aria-label="Orbital Evidence Lens"><div class="evidence-lens-head"><div><div class="evidence-lens-title">Orbital Evidence Lens</div><div class="evidence-lens-subtitle">Official record boundary</div></div><div class="evidence-lens-count">Schema v${esc(e.schemaVersion||1)}</div></div><div class="evidence-lens-signals"><div class="lens-signal"><b>Record type</b><span>${esc(orbitalEvidenceLabel(e.recordType))}</span></div><div class="lens-signal"><b>Architecture role</b><span>${esc(orbitalEvidenceLabel(e.architectureRole))}</span></div><div class="lens-signal"><b>Interpretation</b><span>${esc(orbitalEvidenceLabel(e.interpretationStatus))}</span></div></div><div class="evidence-boundaries"><div class="evidence-boundary supports"><h4>What the record supports</h4><ul>${list(supports)}</ul></div><div class="evidence-boundary limits"><h4>What remains unresolved</h4><ul>${list(unresolved)}</ul></div></div><div class="evidence-lens-foot">Official record · ${esc(e.officialRecord)}</div></section>`;
}
function evidenceLensHtml(c){if(c.mode==='orbital'&&c.orbitalEvidence)return orbitalEvidenceLensHtml(c);const records=lensRecords(c);const record=records.find(r=>(r.supports||[]).length&&(r.limitations||[]).length)||records[0]||{};const supports=(record.supports||[]).slice(0,3),limitations=(record.limitations||[]).slice(0,3),custody=lensCustody(c,records);const list=(items,fallback)=>items.length?items.map(x=>`<li>${esc(x)}</li>`).join(''):`<li>${esc(fallback)}</li>`;return`<section class="evidence-lens" aria-label="Evidence Lens"><div class="evidence-lens-head"><div><div class="evidence-lens-title">Evidence Lens</div><div class="evidence-lens-subtitle">Source boundary before interpretation</div></div><div class="evidence-lens-count">${records.length} mapped record${records.length===1?'':'s'}</div></div><div class="evidence-lens-signals"><div class="lens-signal"><b>Evidence class</b><span>${esc(lensEvidenceClass(c,records))}</span></div><div class="lens-signal" data-tone="${custody.tone}"><b>Custody</b><span>${esc(custody.label)}</span></div><div class="lens-signal"><b>Quote</b><span>${esc(lensQuoteSignal(c))}</span></div></div><div class="evidence-boundaries"><div class="evidence-boundary supports"><h4>What this supports</h4><ul>${list(supports,c.sourceQuality||'Structured source context is mapped.')}</ul></div><div class="evidence-boundary limits"><h4>What it does not establish</h4><ul>${list(limitations,c.gap||'The source does not resolve the full case.')}</ul></div></div><div class="evidence-lens-foot">Boundary source · ${esc(record.citation||record.locator||c.sourceLabel||'Atlas source record')}</div></section>`;}
function heroTypeLabel(v){return String(v||'lead visual').replaceAll('-',' ');}
function evidenceTypeLabel(item){
  if(item.role==='lead') return heroTypeLabel(item.visualType);
  const s=String(item.label||item.src||'');
  if(/__roi_/i.test(s)) return 'ROI';
  if(/contact/i.test(s)) return 'Contact';
  if(/atlas evidence preview|atlas preview/i.test(s)) return 'Reference';
  if(/\.pdf($|\?)/i.test(s)) return 'PDF';
  if(/\.mp4|\.mov|\.webm/i.test(s)) return 'Video';
  return 'Image';
}
function heroActionLabel(h){const u=String(h.mediaUrl||h.sourceUrl||h.src||''); if(/\.(mp4|mov|webm)($|\?)/i.test(u)||/(?:youtube\.com|youtu\.be|dvidshub\.net\/video)/i.test(u)) return 'Watch footage'; if(/\.pdf($|\?)/i.test(u)) return 'Open source file'; if(h.sourceUrl) return 'View source'; return 'Open image';}
function evidenceItems(c){
  const items=[]; const seen=new Set();
  const add=(src,label,kind='image',href=null,rank=50,meta={})=>{if(!src||seen.has(src)) return; seen.add(src); items.push({src,label:label||fileName(src),kind,href:href||src,rank,...meta});};
  const h=c.heroVisual;
  if(h?.src) add(h.src,h.caption||'Case lead visual',h.mediaType||'image',h.mediaUrl||h.sourceUrl||h.src,0,{role:'lead',visualType:h.visualType,provenance:h.provenance||'',evidenceStatus:h.evidenceStatus||'',actionLabel:heroActionLabel(h)});
  (c.sources||[]).forEach(src=>filesForSource(src).forEach(f=>{if(f.kind==='image') add(fileUrl(f.path),`${f.token} · ${fileName(f.path)}`,'image',fileUrl(f.path), /__roi_/i.test(f.path)?30:10,{role:'evidence'});}));
  (c.images||c.evidenceImages||[]).forEach((item,i)=>{
    const structured=item&&typeof item==='object';
    const src=structured?(item.url||item.src):item;
    const label=structured?(item.caption||item.title||`Evidence image ${i+1}`):`Evidence image ${i+1}`;
    const href=structured?(item.sourceUrl||item.source||src):src;
    add(src,label,'image',href,20,{
      role:'evidence',
      visualType:structured?(item.visualType||item.kind||'evidence-image'):'evidence-image',
      provenance:structured?(item.sourceName||item.provenance||''):'',
      evidenceStatus:structured?(item.evidenceStatus||item.rights||''):''
    });
  });
  if(!items.length && c.image){
    const label=/source_previews|robertson_panel/i.test(c.image) ? `Source-derived preview · ${fileName(c.image)}` : 'Atlas preview asset — reference only';
    add(c.image,label,'image',c.image,90,{role:'reference'});
  }
  return items.sort((a,b)=>a.rank-b.rank || evidenceTypeLabel(a).localeCompare(evidenceTypeLabel(b)) || a.label.localeCompare(b.label));
}
function carouselMediaHtml(item){return item.kind==='video'?`<video class="carousel-media" controls preload="metadata" src="${esc(item.src)}"></video>`:`<div class="carousel-media-shell"><img class="carousel-media" src="${esc(item.src)}" alt="${esc(item.label)}" data-lightbox-src="${esc(item.src)}" decoding="async"></div>`;}
function settleCarouselMedia(slot){
  const img=slot?.querySelector('img'); if(!img) return;
  const shell=img.closest('.carousel-media-shell');
  const done=()=>shell?.classList.add('loaded');
  const fail=()=>shell?.classList.add('failed');
  img.addEventListener('load',done,{once:true}); img.addEventListener('error',fail,{once:true});
  if(img.complete){if(img.naturalWidth) done(); else fail();}
  else if(img.decode){img.decode().then(done).catch(()=>{if(img.complete&&img.naturalWidth) done();});}
}
function evidenceCarousel(c){
  const items=evidenceItems(c);
  if(!items.length) return '<div class="drawer-evidence"><div class="carousel-empty">No visual evidence file mapped for this case yet.</div></div>';
  const first=items[0];
  const thumbs=items.map((it,i)=>`<button class="carousel-thumb ${i===0?'active':''}" data-evidence-index="${i}" title="${esc(it.label)}"><img src="${esc(it.kind==='image'?it.src:(c.image||''))}" alt=""><span class="carousel-thumb-label">${esc(it.role==='lead'?'Lead':evidenceTypeLabel(it))}</span></button>`).join('');
  return `<div class="drawer-evidence ${first.role==='lead'?'has-lead':''}" data-carousel="${esc(JSON.stringify(items))}"><div class="carousel-stage">${items.length>1?'<button class="carousel-nav carousel-prev" data-carousel-step="-1" aria-label="Previous evidence">‹</button>':''}<div class="carousel-slot">${carouselMediaHtml(first)}</div>${items.length>1?'<button class="carousel-nav carousel-next" data-carousel-step="1" aria-label="Next evidence">›</button>':''}</div>${items.length>1?`<div class="carousel-thumbs">${thumbs}</div>`:''}</div>`;
}
function publicSourceLinksHtml(c){
  const sources=c.publicSources||[];
  const actionLabel=src=>src.mediaKind==='video'?'Watch video':src.scope==='collection'||src.scope==='official-collection'||src.scope==='official-catalog-collection'?'Search archive':src.role==='official-position'||src.scope==='official-report'?'Read official position':'Open case source';
  const render=src=>`<a class="file-link public-source-link ${src.mediaKind==='video'?'video-source':''}" href="${esc(linkUrl(src.url))}" target="_blank" rel="noopener"><span>${esc(actionLabel(src))}</span><small>${esc(src.label||src.publisher||src.url)}</small>${src.publisher||src.access?`<em>${esc([src.publisher,src.access].filter(Boolean).join(' · '))}</em>`:''}${src.note?`<div class="source-caveat">${esc(src.note)}</div>`:''}</a>`;
  const videos=sources.filter(src=>src.mediaKind==='video');
  const records=sources.filter(src=>src.mediaKind!=='video');
  if(!sources.length) return '';
  const videoRows=videos.length?`<div class="public-source-section"><div class="public-source-section-title">Watch / case analysis</div>${videos.map(render).join('')}</div>`:'';
  const recordRows=records.length?`<div class="public-source-section"><div class="public-source-section-title">Records / research paths</div>${records.map(render).join('')}</div>`:'';
  return `<div class="drawer-source public-source-group"><div class="drawer-source-label">Case sources</div><div class="public-source-note">Videos are witness testimony or contextual analysis—not primary evidence. Official explanations are preserved as institutional positions, not treated as the last word.</div>${videoRows}${recordRows}</div>`;
}
function sourceLinksHtml(c){
  const h=c.heroVisual;
  const heroLinks=h&&h.src?`<div class="drawer-source featured-source"><div class="drawer-source-label">↳ Featured visual · ${esc(heroTypeLabel(h.visualType))}</div><a class="file-link" href="${esc(linkUrl(h.src))}" target="_blank" rel="noopener">View lead image<small>${esc(fileName(h.src))}</small></a>${h.mediaUrl?sourceDisclosureHtml({path:h.mediaUrl,kind:mediaKind(h.mediaUrl)}):''}${h.sourceUrl?`<a class="file-link" href="${esc(linkUrl(h.sourceUrl))}" target="_blank" rel="noopener">View visual source<small>${esc(h.provenance||h.sourceUrl)}</small></a>`:''}<div class="hero-provenance">${esc(h.evidenceStatus||'')}</div></div>`:'';
  const rows=(c.sources||[]).map(src=>{
    const files=filesForSource(src);
    const links=files.map(sourceDisclosureHtml).join('');
    return `<div class="drawer-source"><div class="drawer-source-label">↳ ${esc(src)}</div>${links || '<span class="file-missing">No mapped source asset yet</span>'}</div>`;
  }).join('');
  const preview=c.image?`<div class="drawer-source"><div class="drawer-source-label">↳ Atlas preview asset</div><a class="file-link" href="${esc(c.image)}" target="_blank" rel="noopener">View Atlas preview<small>${esc(fileName(c.image))}</small></a></div>`:'';
  return `<div class="source-links">${publicSourceLinksHtml(c)}${heroLinks}${rows || '<p class="drawer-summary">No source trail listed.</p>'}${preview}</div>`;
}
function initCarousel(drawer){
  const root=drawer.querySelector('[data-carousel]'); if(!root) return;
  const items=JSON.parse(root.dataset.carousel); let idx=0;
  const slot=root.querySelector('.carousel-slot');
  settleCarouselMedia(slot);
  const show=i=>{idx=(i+items.length)%items.length; const it=items[idx]; slot.innerHTML=carouselMediaHtml(it); settleCarouselMedia(slot); root.classList.toggle('has-lead',it.role==='lead'); root.querySelectorAll('[data-evidence-index]').forEach((b,n)=>b.classList.toggle('active',n===idx));};
  root.querySelectorAll('[data-carousel-step]').forEach(btn=>btn.addEventListener('click',()=>show(idx+Number(btn.dataset.carouselStep))));
  root.querySelectorAll('[data-evidence-index]').forEach(btn=>btn.addEventListener('click',()=>show(Number(btn.dataset.evidenceIndex))));
  root.addEventListener('click',e=>{const img=e.target.closest('[data-lightbox-src]'); if(img) openLightbox(img.dataset.lightboxSrc,img.alt,items,idx);});
}
function ensureLightbox(){let lb=document.getElementById('imageLightbox'); if(lb) return lb; document.body.insertAdjacentHTML('beforeend','<div class="lightbox" id="imageLightbox"><div class="lightbox-frame"><button class="lightbox-nav lightbox-prev" data-lb-step="-1" aria-label="Previous image">‹</button><button class="lightbox-nav lightbox-next" data-lb-step="1" aria-label="Next image">›</button><div class="lightbox-tools"><button data-lb="out" aria-label="Zoom out">−</button><button data-lb="in" aria-label="Zoom in">+</button><button data-lb="reset">100%</button><a data-lb-link href="#" target="_blank" rel="noopener">Open file</a><button data-lb="close" aria-label="Close image viewer">×</button></div><img class="lightbox-img" alt="Full size evidence"><div class="lightbox-status" data-lb-status></div></div></div>'); return document.getElementById('imageLightbox');}
function openLightbox(src,alt='Evidence image',carouselItems=[],carouselIndex=0){
  const lb=ensureLightbox(), img=lb.querySelector('.lightbox-img'), link=lb.querySelector('[data-lb-link]'), status=lb.querySelector('[data-lb-status]'); const visuals=carouselItems.filter(it=>it.kind==='image'); let current=Math.max(0,visuals.findIndex(it=>it.src===src)); let zoom=1, pan={x:0,y:0}, dragging=false, start=null;
  const apply=()=>{img.style.transform=`translate(${pan.x}px,${pan.y}px) scale(${zoom})`;};
  const show=i=>{if(!visuals.length) return; current=(i+visuals.length)%visuals.length; const it=visuals[current]; zoom=1; pan={x:0,y:0}; img.src=it.src; img.alt=it.label||alt; link.href=it.href||it.src; status.textContent=`${current+1} / ${visuals.length} · ${it.label||'Evidence image'}`; apply();};
  if(!visuals.length) visuals.push({src,label:alt,href:src,kind:'image'});
  lb.querySelectorAll('[data-lb-step]').forEach(btn=>{btn.hidden=visuals.length<2; btn.onclick=()=>show(current+Number(btn.dataset.lbStep));});
  show(current); lb.classList.add('open');
  lb.querySelector('[data-lb="in"]').onclick=()=>{zoom=clamp(zoom+.35,1,5); apply();};
  lb.querySelector('[data-lb="out"]').onclick=()=>{zoom=clamp(zoom-.35,1,5); if(zoom===1) pan={x:0,y:0}; apply();};
  lb.querySelector('[data-lb="reset"]').onclick=()=>{zoom=1; pan={x:0,y:0}; apply();};
  lb.querySelector('[data-lb="close"]').onclick=()=>lb.classList.remove('open');
  lb.onclick=e=>{if(e.target===lb) lb.classList.remove('open');};
  img.onmousedown=e=>{if(zoom<=1) return; dragging=true; start={x:e.clientX-pan.x,y:e.clientY-pan.y}; e.preventDefault();};
  window.onmousemove=e=>{if(!dragging) return; pan={x:e.clientX-start.x,y:e.clientY-start.y}; apply();};
  window.onmouseup=()=>{dragging=false;};
  img.onwheel=e=>{e.preventDefault(); zoom=clamp(zoom+(e.deltaY<0?.28:-.28),1,5); if(zoom===1) pan={x:0,y:0}; apply();};
}
let drawerReturnFocus=null;
function openFullCase(id){
  const c=cases.find(x=>x.id===id); if(!c) return;
  const drawer=document.getElementById('caseDrawer'), backdrop=document.getElementById('drawerBackdrop');
  if(!backdrop.classList.contains('open')) drawerReturnFocus=document.activeElement;
  const navList=visibleStackCases();
  const navPos=navList.findIndex(x=>x.id===id);
  drawer.innerHTML=`<div class="drawer-header"><div class="drawer-heading"><div class="eyebrow">${esc(c.id)} · ${esc(c.mode)} · ${esc(c.domain)}</div><div class="case-title">${esc(c.title)}</div><div class="loc">${esc(c.date)} · ${esc(c.location)} · ${esc(c.agency)}</div></div><div class="drawer-nav">${navPos>=0&&navList.length>1?`<button class="drawer-navbtn" type="button" data-drawer-nav="-1" aria-label="Previous case">‹</button><span class="drawer-pos">${navPos+1} / ${navList.length}</span><button class="drawer-navbtn" type="button" data-drawer-nav="1" aria-label="Next case">›</button>`:''}<button class="drawer-close" aria-label="Close full case file">×</button></div></div>${evidenceCarousel(c)}<div class="pills"><span class="pill ${statusPill[markerStatus(c)]}">${esc(c.status)}</span><span class="pill">${esc(compactConfidence(c.confidence))}</span></div><div class="drawer-tabs"><button class="drawer-tab active" data-tab="brief">BRIEF</button><button class="drawer-tab" data-tab="timeline">TIMELINE</button><button class="drawer-tab" data-tab="official">OFFICIAL POSITION</button><button class="drawer-tab" data-tab="gaps">RECORD GAPS</button><button class="drawer-tab" data-tab="sources">FILES / SOURCES</button></div><section class="drawer-panel active" data-panel="brief">${c.summary?`<div class="dossier-summary"><b>Case summary</b><p>${esc(c.summary)}</p></div>`:''}${keyFactHtml(c,true)}${evidenceLensHtml(c)}${culturalLegacyHtml(c)}${briefFooterStrip(c)}${relatedRecordsHtml(c)}</section><section class="drawer-panel" data-panel="timeline">${drawerTimeline(c.id)}</section><section class="drawer-panel" data-panel="official"><div class="drawer-box"><h4>Public / official position</h4><p>${esc(c.official)}</p></div></section><section class="drawer-panel" data-panel="gaps"><div class="drawer-box"><h4>What is still missing</h4><p>${esc(c.gap)}</p></div></section><section class="drawer-panel" data-panel="sources">${sourceLinksHtml(c)}</section>`;
  backdrop.classList.add('open');
  initCarousel(drawer);

  drawer.scrollTop=0;
  drawer.querySelector('.drawer-close').addEventListener('click',closeFullCase);
  drawer.querySelector('.drawer-close').focus({preventScroll:true});
  drawer.querySelectorAll('[data-drawer-nav]').forEach(btn=>btn.addEventListener('click',()=>{
    const list=visibleStackCases(); if(!list.length) return;
    let i=list.findIndex(x=>x.id===state.selectedCaseId); if(i<0) i=0;
    i=(i+Number(btn.dataset.drawerNav)+list.length)%list.length;
    selectCase(list[i].id,false); openFullCase(list[i].id);
  }));
  drawer.querySelectorAll('[data-tab]').forEach(btn=>btn.addEventListener('click',()=>{drawer.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===btn)); drawer.querySelectorAll('[data-panel]').forEach(p=>p.classList.toggle('active',p.dataset.panel===btn.dataset.tab));}));
  drawer.querySelectorAll('[data-related-case]').forEach(btn=>btn.addEventListener('click',()=>{selectCase(btn.dataset.relatedCase,true); openFullCase(btn.dataset.relatedCase);}));
  urlCaseId=id;
  updateUrl();
}
function closeFullCase(){document.getElementById('drawerBackdrop').classList.remove('open'); urlCaseId=null; updateUrl(); if(drawerReturnFocus&&document.contains(drawerReturnFocus)){drawerReturnFocus.focus({preventScroll:true});} drawerReturnFocus=null;}

/* URL state — hash-based links preserve app state */
let urlCaseId=null, lastWrittenHash='';
function updateUrl(){
  const p=new URLSearchParams();
  if(state.filters.agency!=='all') p.set('agency',state.filters.agency);
  if(state.filters.domain!=='all') p.set('domain',state.filters.domain);
  if(state.filters.precision!=='all') p.set('precision',state.filters.precision);
  if(state.filters.q) p.set('q',state.filters.q);
  if(state.filters.era!=='all') p.set('era',String(state.filters.era));
  if(state.stackMode==='orbital') p.set('view','orbital');
  if(!state.institutional) p.set('inst','off');
  if(urlCaseId) p.set('case',urlCaseId);
  const qs=p.toString();
  lastWrittenHash=qs?'#'+qs:'';
  try{history.replaceState(null,'',location.pathname+location.search+lastWrittenHash);}
  catch(_){location.hash=lastWrittenHash;}
}
window.addEventListener('hashchange',()=>{
  if(location.hash===lastWrittenHash) return; // our own write, not an incoming link
  agencyFilter.value='all'; domainFilter.value='all'; precisionFilter.value='all';
  state.filters={agency:'all',domain:'all',precision:'all',q:'',era:'all'};
  state.stackMode='main';
  const cs=document.getElementById('caseSearch'); if(cs) cs.value='';
  state.institutional=true; toggleInstitutional.textContent='Institutional: ON'; toggleInstitutional.classList.add('active');
  urlCaseId=null;
  parseUrlState();
  if(typeof buildEraRail==='function') buildEraRail();
  renderAll();
  if(urlCaseId && cases.some(c=>c.id===urlCaseId)){selectCase(urlCaseId,true); openFullCase(urlCaseId);}
  else closeFullCase();
});
function parseUrlState(){
  let h=location.hash.replace(/^#\/?/,'');
  if(!h) return;
  if(h.startsWith('case/')){urlCaseId=decodeURIComponent(h.slice(5)); const linked=cases.find(c=>c.id===urlCaseId); if(linked) state.stackMode=stackModeForCase(linked); return;} // legacy format
  const p=new URLSearchParams(h);
  const pick=(el,v)=>{if(v&&[...el.options].some(o=>o.value===v)) el.value=v;};
  pick(agencyFilter,p.get('agency')); pick(domainFilter,p.get('domain')); pick(precisionFilter,p.get('precision'));
  state.filters.agency=agencyFilter.value; state.filters.domain=domainFilter.value; state.filters.precision=precisionFilter.value;
  if(p.get('q')){state.filters.q=p.get('q').trim().toLowerCase(); const cs=document.getElementById('caseSearch'); if(cs) cs.value=p.get('q');}
  if(p.get('era')&&/^\d{4}$/.test(p.get('era'))) state.filters.era=Number(p.get('era'));
  if(p.get('view')==='orbital') state.stackMode='orbital';
  if(p.get('inst')==='off'){state.institutional=false; toggleInstitutional.textContent='Institutional: OFF';}
  urlCaseId=p.get('case');
  if(urlCaseId){const linked=cases.find(c=>c.id===urlCaseId); if(linked) state.stackMode=stackModeForCase(linked);}
}
document.getElementById('drawerBackdrop').addEventListener('click',e=>{if(e.target.id==='drawerBackdrop') closeFullCase();});
document.addEventListener('keydown',e=>{const lb=document.getElementById('imageLightbox'); if(lb&&lb.classList.contains('open')){if(e.key==='Escape'){lb.classList.remove('open'); return;} if(e.key==='ArrowLeft'||e.key==='ArrowRight'){lb.querySelector(`[data-lb-step="${e.key==='ArrowLeft'?'-1':'1'}"]`)?.click(); e.preventDefault(); return;}} if(e.key==='Escape') closeFullCase();});

function selectCase(id,zoom){
  state.selectedCaseId=id;
  const c=cases.find(x=>x.id===id);
  if(!c) return;
  const desiredMode=stackModeForCase(c);
  if(state.stackMode!==desiredMode) state.stackMode=desiredMode;
  state.selectedEventId=(events.find(e=>e.caseId===id)||{}).id||state.selectedEventId;
  if(zoom){ if(markerStatus(c)==='orbital') resetView(); else zoomToCase(c.x,c.y,6.25); }
  renderAll();
  highlightRow(id);
  renderSelectionBeacon(Boolean(zoom));
  setTimeout(()=>{
    const row=document.querySelector(`.case-row[data-id="${CSS.escape(id)}"]`);
    if(row){row.scrollIntoView({block:'start',inline:'nearest'}); const rr=row.getBoundingClientRect(), lr=caseList.getBoundingClientRect(); if(rr.top<lr.top) caseList.scrollTop -= (lr.top-rr.top+8);}
    /* No scrollIntoView for timeline nodes — the signal band spans full width, no scroll */
  },50);
}
function highlightRow(id){caseList.querySelectorAll('.case-row').forEach(el=>el.classList.toggle('active', el.dataset.id===id)); nodeLayer.querySelectorAll('.signal-node').forEach(el=>el.classList.toggle('selected', el.dataset.event===state.selectedEventId)); markersG.querySelectorAll('.atlas-marker').forEach(el=>el.classList.toggle('selected', el.dataset.id===id));}
function renderAll(){renderCaseGeometry(); renderMarkers(); renderClusters(); renderCaseList(); renderSignal(); renderDetail(); highlightRow(state.selectedCaseId); renderSelectionBeacon(false);}
function resetAtlasHome(){
  cancelViewAnim();
  stopEraPlay();
  resetStackFilters();
  state.stackMode='main';
  state.selectedCaseId=null;
  state.selectedEventId=null;
  state.institutional=true;
  toggleInstitutional.textContent='Institutional: ON';
  toggleInstitutional.classList.add('active');
  urlCaseId=null;
  document.getElementById('drawerBackdrop').classList.remove('open');
  document.getElementById('imageLightbox')?.classList.remove('open');
  document.dispatchEvent(new CustomEvent('atlas:home-reset'));
  renderAll();
  resetView();
  updateUrl();
}
window.resetAtlasHome=resetAtlasHome;
document.getElementById('atlasHome').addEventListener('click',resetAtlasHome);
function applyFilters(){state.filters.agency=agencyFilter.value; state.filters.domain=domainFilter.value; state.filters.precision=precisionFilter.value; renderAll(); updateUrl();}
agencyFilter.addEventListener('change',applyFilters); domainFilter.addEventListener('change',applyFilters); precisionFilter.addEventListener('change',applyFilters); if(stackReturn) stackReturn.addEventListener('click',()=>{resetStackFilters(); setStackMode('main');}); toggleInstitutional.addEventListener('click',()=>{state.institutional=!state.institutional; toggleInstitutional.textContent = `Institutional: ${state.institutional?'ON':'OFF'}`; toggleInstitutional.classList.toggle('active', state.institutional); renderSignal(); updateUrl();});
svg.addEventListener('wheel',e=>{e.preventDefault(); cancelViewAnim(); const pt = svg.createSVGPoint(); pt.x=e.clientX; pt.y=e.clientY; const ctm=svg.getScreenCTM().inverse(); const p=pt.matrixTransform(ctm); const factor = e.deltaY>0 ? 1.12 : 0.89; const nw = clamp(state.view.w*factor, 8, 100); const nh = nw*0.62; const mx = (p.x-state.view.x)/state.view.w, my = (p.y-state.view.y)/state.view.h; const x = clamp(p.x - mx*nw, 0, 100-nw); const y = clamp(p.y - my*nh, 0, 62-nh); setView(x,y,nw);},{passive:false});
svg.addEventListener('mousedown',e=>{cancelViewAnim(); hideMapTip(); state.dragging=true; state.dragStart={x:e.clientX,y:e.clientY,view:{...state.view}};}); window.addEventListener('mousemove',e=>{if(!state.dragging) return; const dx=(e.clientX-state.dragStart.x)/svg.clientWidth*state.dragStart.view.w; const dy=(e.clientY-state.dragStart.y)/svg.clientHeight*state.dragStart.view.h; setView(clamp(state.dragStart.view.x-dx,0,100-state.dragStart.view.w), clamp(state.dragStart.view.y-dy,0,62-state.dragStart.view.h), state.dragStart.view.w);}); window.addEventListener('mouseup',()=>state.dragging=false);
document.querySelectorAll('[data-zoom]').forEach(btn=>btn.addEventListener('click',()=>{if(btn.dataset.zoom==='reset') return resetView(); if(btn.dataset.zoom==='in') zoomToCase(state.view.x+state.view.w/2,state.view.y+state.view.h/2, currentZoom()*1.35); else zoomToCase(state.view.x+state.view.w/2,state.view.y+state.view.h/2, currentZoom()/1.35);}));
window.selectCase = selectCase;
const caseSearch=document.getElementById('caseSearch');
if(caseSearch){
  caseSearch.addEventListener('input',()=>{state.filters.q=caseSearch.value.trim().toLowerCase(); renderAll(); updateUrl();});
  caseSearch.addEventListener('keydown',e=>{
    if(e.key==='Escape'&&caseSearch.value){caseSearch.value=''; state.filters.q=''; renderAll(); e.stopPropagation();}
  });
}
document.addEventListener('keydown',e=>{
  if(e.key!=='ArrowDown'&&e.key!=='ArrowUp'&&e.key!=='Enter') return;
  const tag=(e.target.tagName||'').toLowerCase();
  if(tag==='input'||tag==='select'||tag==='textarea') return;
  if(e.key==='Enter'&&(tag==='button'||e.target.closest?.('.case-row'))) return;
  const list=visibleStackCases(); if(!list.length) return;
  const drawerOpen=document.getElementById('drawerBackdrop').classList.contains('open');
  if(e.key==='Enter'){ if(!drawerOpen&&state.selectedCaseId) openFullCase(state.selectedCaseId); return; }
  e.preventDefault();
  let i=list.findIndex(c=>c.id===state.selectedCaseId);
  i=(i+(e.key==='ArrowDown'?1:-1)+list.length)%list.length;
  selectCase(list[i].id,false);
  if(drawerOpen) openFullCase(list[i].id);
});
const dataStrip=document.getElementById('dataStrip');
if(dataStrip){
  const agencies=new Set(cases.map(c=>c.agency)).size;
  const records=Object.keys(sourceFileIndex).length;
  dataStrip.innerHTML=`<span><b>${cases.length}</b> cases</span><span><b>${events.length}</b> events</span><span><b>${agencies}</b> agencies</span><span><b>${records}</b> records</span>`;
}
const syncClock=document.getElementById('syncClock');
if(syncClock){const tick=()=>{syncClock.textContent=new Date().toLocaleTimeString('en-GB',{hour12:false});}; tick(); setInterval(tick,1000);}
/* Era rail — decade scrubber linking the temporal signal to the map */
const eraRail=document.getElementById('eraRail');
const decades=[...new Set(cases.map(c=>Math.floor(c.year/10)*10))].sort((a,b)=>a-b);
let eraTimer=null;
function buildEraRail(){
  if(!eraRail) return;
  eraRail.innerHTML=`<button class="era-chip ${state.filters.era==='all'?'active':''}" type="button" data-era="all">All</button>`
    +decades.map(d=>`<button class="era-chip ${state.filters.era===d?'active':''}" type="button" data-era="${d}">${String(d).slice(2)}s</button>`).join('')
    +`<button class="era-play" id="eraPlay" type="button" aria-label="Play era sequence" title="Play era sequence">▸</button>`;
  eraRail.querySelectorAll('.era-chip').forEach(b=>b.addEventListener('click',()=>{stopEraPlay(); setEra(b.dataset.era==='all'?'all':Number(b.dataset.era));}));
  document.getElementById('eraPlay').addEventListener('click',toggleEraPlay);
}
function setEra(era){
  state.filters.era=era;
  markersG.classList.add('era-anim');
  setTimeout(()=>markersG.classList.remove('era-anim'),700);
  renderAll(); updateUrl();
  eraRail.querySelectorAll('.era-chip').forEach(b=>b.classList.toggle('active', b.dataset.era===String(era)));
  if(era!=='all'){
    /* No horizontal scroll in the new band; the signal canvas spans full width */
  }
}
function toggleEraPlay(){
  if(eraTimer) return stopEraPlay();
  const btn=document.getElementById('eraPlay');
  btn.textContent='■'; btn.classList.add('on');
  let i=0; setEra(decades[0]);
  eraTimer=setInterval(()=>{
    i++;
    if(i>=decades.length){stopEraPlay(); setEra('all'); return;}
    setEra(decades[i]);
  },1600);
}
function stopEraPlay(){
  if(eraTimer){clearInterval(eraTimer); eraTimer=null;}
  const btn=document.getElementById('eraPlay');
  if(btn){btn.textContent='▸'; btn.classList.remove('on');}
}

buildFilters(); renderLabels();
parseUrlState();
buildEraRail();
renderAll(); resetView();
if(urlCaseId && cases.some(c=>c.id===urlCaseId)){ selectCase(urlCaseId,true); openFullCase(urlCaseId); }
else selectCase((visibleStackCases()[0]||stackBaseCases()[0]||cases[0]).id,false);
/* ATLAS_MOBILE_JS_START */

/* Atlas Mobile three-page controller */
let mobilePage='map';
const mobilePages=new Set(['map','cases','dossier']);
const mobileMedia=matchMedia('(max-width:1080px)');
const isMobileAtlas=()=>mobileMedia.matches;
function renderMobilePeek(){
  const c=cases.find(x=>x.id===state.selectedCaseId);
  const meta=document.getElementById('peekMeta'), title=document.getElementById('peekTitle'), loc=document.getElementById('peekLoc');
  if(!meta||!title||!loc) return;
  if(!c){meta.textContent='Select a case';title.textContent='Tap a map marker';loc.textContent='The selected file will appear here.';return;}
  meta.textContent=`${c.id} · ${c.date}`; title.textContent=c.title; loc.textContent=`${c.location} · ${c.agency}`;
}
function normalizeMobileDossier(){
  const drawer=document.getElementById('caseDrawer');
  if(!drawer) return;
  if(!drawer.querySelector('.mobile-dossier-home')) drawer.insertAdjacentHTML('afterbegin','<button class="mobile-dossier-home" type="button" aria-label="Reset UAP Atlas to home"><span class="aperture-logo" aria-hidden="true"></span><span class="brand-primary">Cortana</span><i></i><span class="brand-secondary">UAP Case Atlas</span></button>');
  drawer.querySelector('.mobile-dossier-home').onclick=resetAtlasHome;
  const brief=drawer.querySelector('[data-panel="brief"]');
  const official=drawer.querySelector('[data-panel="official"] .drawer-box');
  const gaps=drawer.querySelector('[data-panel="gaps"] .drawer-box');
  if(brief&&!brief.querySelector('.mobile-brief-context')){
    const context=document.createElement('div');
    context.className='mobile-brief-context';
    if(official) context.append(official.cloneNode(true));
    if(gaps) context.append(gaps.cloneNode(true));
    brief.append(context);
  }
  drawer.querySelectorAll('[data-tab="official"],[data-tab="gaps"],[data-panel="official"],[data-panel="gaps"]').forEach(el=>el.remove());
  const c=cases.find(x=>x.id===state.selectedCaseId);
  const pills=drawer.querySelector(':scope > .pills');
  if(c&&pills&&!drawer.querySelector('.mobile-status')){
    pills.insertAdjacentHTML('afterend',`<div class="mobile-status"><b>${esc(c.status)}</b><i>·</i>${esc(compactConfidence(c.confidence))}</div>`);
  }
}
function syncMobileNav(){
  document.body.dataset.mobilePage=mobilePage;
  document.querySelectorAll('.mobile-nav [data-page]').forEach(btn=>{
    const active=btn.dataset.page===mobilePage; btn.classList.toggle('active',active); btn.setAttribute('aria-current',active?'page':'false');
  });
  if(mobilePage!=='map') document.body.classList.remove('map-immersive');
}
function setMobilePage(page,{write=true}={}){
  mobilePage=mobilePages.has(page)?page:'map';
  if(mobilePage==='dossier'){
    const id=state.selectedCaseId||(visibleStackCases()[0]||cases[0]||{}).id;
    if(id) openFullCase(id);
  }else{
    document.getElementById('drawerBackdrop')?.classList.remove('open');
    urlCaseId=null;
    drawerReturnFocus=null;
  }
  syncMobileNav(); renderMobilePeek();
  if(write) updateUrl();
}
document.querySelectorAll('.mobile-nav [data-page]').forEach(btn=>btn.addEventListener('click',()=>setMobilePage(btn.dataset.page)));
document.getElementById('peekOpen')?.addEventListener('click',()=>setMobilePage('dossier'));
document.addEventListener('atlas:home-reset',()=>{mobilePage='map';syncMobileNav();renderMobilePeek();});
function focusMobileCaseFromStack(id){
  selectCase(id,true);
  setMobilePage('map');
}
caseList.addEventListener('click',e=>{
  if(!isMobileAtlas()) return;
  const row=e.target.closest('.case-row'); if(!row) return;
  const id=row.dataset.id;
  e.preventDefault(); e.stopPropagation();
  focusMobileCaseFromStack(id);
},true);
caseList.addEventListener('keydown',e=>{
  if(!isMobileAtlas()) return;
  if(e.key!=='Enter'&&e.key!==' ') return;
  const row=e.target.closest('.case-row'); if(!row) return;
  const id=row.dataset.id;
  e.preventDefault(); e.stopPropagation();
  focusMobileCaseFromStack(id);
},true);
const mapFullscreen=document.querySelector('[data-map-fullscreen]');
async function toggleMapImmersive(){
  const entering=!document.body.classList.contains('map-immersive');
  document.body.classList.toggle('map-immersive',entering);
  if(entering&&document.documentElement.requestFullscreen){try{await document.documentElement.requestFullscreen();}catch(_){}}
  else if(!entering&&document.fullscreenElement&&document.exitFullscreen){try{await document.exitFullscreen();}catch(_){}}
  mapFullscreen?.setAttribute('aria-label',entering?'Exit full-screen map':'Open full-screen map');
  setTimeout(()=>setView(state.view.x,state.view.y,state.view.w),80);
}
mapFullscreen?.addEventListener('click',toggleMapImmersive);
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement) document.body.classList.remove('map-immersive');});

/* Pointer-based pan + pinch for iPhone. Mouse keeps the established handlers. */
const mapPointers=new Map(); let pinchStart=null;
svg.addEventListener('pointerdown',e=>{
  if(!isMobileAtlas()||e.pointerType==='mouse') return;
  e.preventDefault(); svg.setPointerCapture?.(e.pointerId); cancelViewAnim();
  mapPointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(mapPointers.size===1) state.dragStart={x:e.clientX,y:e.clientY,view:{...state.view}};
  if(mapPointers.size===2){const p=[...mapPointers.values()];pinchStart={distance:Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y),view:{...state.view},center:{x:(p[0].x+p[1].x)/2,y:(p[0].y+p[1].y)/2}};}
},{passive:false});
svg.addEventListener('pointermove',e=>{
  if(!isMobileAtlas()||!mapPointers.has(e.pointerId)||e.pointerType==='mouse') return;
  e.preventDefault(); mapPointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(mapPointers.size===2&&pinchStart){
    const p=[...mapPointers.values()],dist=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);
    const nw=clamp(pinchStart.view.w*(pinchStart.distance/Math.max(1,dist)),8,100),nh=nw*.62;
    const rect=svg.getBoundingClientRect(),rx=(pinchStart.center.x-rect.left)/rect.width,ry=(pinchStart.center.y-rect.top)/rect.height;
    const anchorX=pinchStart.view.x+rx*pinchStart.view.w,anchorY=pinchStart.view.y+ry*pinchStart.view.h;
    setView(clamp(anchorX-rx*nw,0,100-nw),clamp(anchorY-ry*nh,0,62-nh),nw); return;
  }
  if(mapPointers.size===1&&state.dragStart){
    const dx=(e.clientX-state.dragStart.x)/svg.clientWidth*state.dragStart.view.w,dy=(e.clientY-state.dragStart.y)/svg.clientHeight*state.dragStart.view.h;
    setView(clamp(state.dragStart.view.x-dx,0,100-state.dragStart.view.w),clamp(state.dragStart.view.y-dy,0,62-state.dragStart.view.h),state.dragStart.view.w);
  }
},{passive:false});
function releaseMapPointer(e){mapPointers.delete(e.pointerId);if(mapPointers.size<2)pinchStart=null;if(mapPointers.size===1){const p=[...mapPointers.values()][0];state.dragStart={x:p.x,y:p.y,view:{...state.view}};}else if(!mapPointers.size)state.dragStart=null;}
svg.addEventListener('pointerup',releaseMapPointer);svg.addEventListener('pointercancel',releaseMapPointer);

/* Fold mobile page state into the existing hash model. */
const desktopUpdateUrl=updateUrl;
updateUrl=function(){
  desktopUpdateUrl();
  if(!isMobileAtlas()) return;
  const h=location.hash.replace(/^#/,''); const p=new URLSearchParams(h); p.set('page',mobilePage);
  const next='#'+p.toString(); lastWrittenHash=next; try{history.replaceState(null,'',location.pathname+location.search+next);}catch(_){location.hash=next;}
};
const originalOpenFullCase=openFullCase;
openFullCase=function(id){
  originalOpenFullCase(id);
  if(!isMobileAtlas()) return;
  mobilePage='dossier';normalizeMobileDossier();syncMobileNav();renderMobilePeek();
};
const originalCloseFullCase=closeFullCase;
closeFullCase=function(){if(isMobileAtlas()){setMobilePage('cases');return;}originalCloseFullCase();};
const originalSelectCase=selectCase;
selectCase=function(id,zoom){originalSelectCase(id,zoom);renderMobilePeek();};

const initialMobileParams=new URLSearchParams(location.hash.replace(/^#\/?/,''));
mobilePage=mobilePages.has(initialMobileParams.get('page'))?initialMobileParams.get('page'):(urlCaseId?'dossier':'map');
syncMobileNav();renderMobilePeek();
if(isMobileAtlas()&&mobilePage==='dossier'&&state.selectedCaseId){originalOpenFullCase(state.selectedCaseId);normalizeMobileDossier();}

/* ATLAS_MOBILE_JS_END */
