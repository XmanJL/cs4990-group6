// ── French stemmed word → English translation ─────────────────────────────
// Keys are what SnowballStemmer("french") produces; extend freely.
const FR_TRANSLATIONS = {
    "joueur":"player","vol":"shuttlecock","badminton":"badminton","doubl":"doubles",
    "raquet":"racket","point":"point","class":"classification","filet":"net",
    "terrain":"court/field","servic":"service","simpl":"singles","jeu":"game/play",
    "match":"match","niveau":"level","serv":"serves","lign":"line","sont":"are",
    "doit":"must","frapp":"hit/strike","équip":"team/equipment","été":"been/was",
    "pratiqu":"practice","haut":"high/top","sport":"sport","deux":"two",
    "homm":"men","droit":"right/straight","depuis":"since","utilis":"used",
    "mond":"world","dam":"women/ladies","dame":"women/ladies","pend":"during",
    "lors":"during/when","disciplin":"discipline","championnat":"championship",
    "chaqu":"each/every","coup":"shot/stroke","mixt":"mixed","plum":"feather",
    "gagn":"win/gain","set":"set","adversair":"opponent","fédér":"federation",
    "échang":"rally/exchange","échange":"rally/exchange","dessu":"above",
    "zon":"zone","zone":"zone","olympiqu":"olympic","règl":"rule","scor":"score",
    "moyen":"average","moyenn":"average","plac":"place","faut":"fault/must",
    "touch":"touch","trajectoir":"trajectory","lorsqu":"when","mont":"rise/climb",
    "demi":"half","court":"court","contr":"against","sert":"serves","fond":"back",
    "arbitr":"referee/umpire","mètr":"metre","drapeau":"flag","séri":"series",
    "bwf":"BWF","rapid":"fast","vitess":"speed","an":"years","ans":"years",
    "main":"hand","jeux":"games (Olympic)","seul":"only","limit":"limit",
    "amorti":"drop shot","classement":"ranking","final":"final","soit":"either/be",
    "pair":"pair","corp":"body","peut":"can/may","plus":"more","si":"if",
    "jou":"play","serveur":"server"
};

// Colour palette matching the matplotlib viridis-style scheme in the images
const PALETTE = [
  "#1f4e79","#2980b9","#1a7a4a","#2e8b57","#6db33f","#9ec93a","#c8dc3a",
  "#7b2d8b","#8e44ad","#4a1060","#1e6fa0","#27ae60","#82e0aa","#a9cce3",
  "#5b2c6f","#884ea0","#d4ac0d","#f39c12","#ca6f1e","#dc7633","#2874a6",
  "#148f77","#1abc9c","#16a085","#2471a3","#1f618d","#117a65","#0e6655",
  "#186a3b","#1d8348"
];
const getColor = i => PALETTE[i % PALETTE.length];

// ── App state ──────────────────────────────────────────────────────────────
// DATA shape from export_json(): { en: [{word, count, tf, idf, tfidf},...], fr: [...] }
let DATA = null;
let lang = 'en';
let zoom = 1, panX = 0, panY = 0;
let words = [];
let selected = null, hovered = null;
let draggingCanvas = false, draggingWord = null;
let dragCvX, dragCvY, panSX, panSY;
let wdOfsX, wdOfsY;
let mdX = 0, mdY = 0, didMove = false;

const wrap    = document.getElementById('canvas-wrap');
const canvas  = document.getElementById('c');
const ctx     = canvas.getContext('2d');
const overlay = document.getElementById('overlay');

// ── Data loading ───────────────────────────────────────────────────────────
// Reads wordcloud_data.json written by main.py → export_json().
// If the file is missing, a clear error is shown explaining how to generate it.
async function loadData() {
  try {
    const res = await fetch('../../results/project2/wordcloud_data.json');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    DATA = await res.json();
    overlay.classList.add('hidden');
    init();
  } catch (err) {
    overlay.querySelector('.spinner').style.display = 'none';
    overlay.innerHTML = `
      <div class="err">
        ⚠️ Could not load <code>../../results/project2/wordcloud_data.json</code>.<br><br>
        Run the Python pipeline first to generate it:<br><br>
        <code>python main.py</code><br><br>
        Then serve this folder locally, e.g.:<br>
        <code>python -m http.server 8000</code><br>
        and open <code>http://localhost:8000</code>
      </div>`;
  }
}

// ── Font sizing (mirrors Counter frequency weighting in visualize.py) ──────
function fontSize(count, maxC, minC) {
  const t = Math.pow((count - minC) / Math.max(1, maxC - minC), 0.5);
  return Math.round(10 + t * 74); // 10–84 px
}

// ── Layout ─────────────────────────────────────────────────────────────────
// ~20% vertical words, matching matplotlib wordcloud's default orientation mix
const ANGLE_PAT = [0,0,0,0,0,0,90,0,0,0,90,0,0,0,0,90,0,0,0,0];

function layout() {
  const data = DATA[lang];
  const maxC = data[0].count, minC = data[data.length - 1].count;
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  words = [];
  const boxes = [];

  const sc = document.createElement('canvas').getContext('2d');

  for (let i = 0; i < data.length; i++) {
    const item  = data[i];
    const fs    = fontSize(item.count, maxC, minC);
    const angle = ANGLE_PAT[i % ANGLE_PAT.length];
    const color = getColor(i);

    sc.font = `bold ${fs}px Arial`;
    const tw = sc.measureText(item.word).width;
    const th = fs * 1.1;
    const bw = angle === 90 ? th     : tw + 2;
    const bh = angle === 90 ? tw + 2 : th;

    let placed = false;
    for (let step = 0; step < 10000; step++) {
      const r  = 0.8 * step;
      const bx = cx + r * Math.cos(step * 0.15) - bw / 2;
      const by = cy + r * 0.65 * Math.sin(step * 0.15) - bh / 2;

      let ok = true;
      for (const b of boxes)
        if (bx < b.x+b.w+2 && bx+bw+2 > b.x && by < b.y+b.h+2 && by+bh+2 > b.y) { ok=false; break; }

      if (ok) {
        boxes.push({ x:bx, y:by, w:bw, h:bh });
        // carry idf and tfidf from JSON into each word object
        words.push({ word:item.word, count:item.count, tf:item.tf,
                     idf:item.idf, tfidf:item.tfidf, rank:i+1,
                     fs, angle, color, tw, th, bx, by, bw, bh,
                     dragDx:0, dragDy:0, hovered:false, selected:false });
        placed = true; break;
      }
    }

    if (!placed) {  // fallback scatter
      const bx = cx + (Math.random()-0.5)*W*0.9;
      const by = cy + (Math.random()-0.5)*H*0.9;
      boxes.push({ x:bx, y:by, w:bw, h:bh });
      words.push({ word:item.word, count:item.count, tf:item.tf,
                   idf:item.idf, tfidf:item.tfidf, rank:i+1,
                   fs, angle, color, tw, th, bx, by, bw, bh,
                   dragDx:0, dragDy:0, hovered:false, selected:false });
    }
  }
}

// ── Draw ───────────────────────────────────────────────────────────────────
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.translate(panX, panY);
  ctx.scale(zoom, zoom);

  for (const w of words) {
    const bx = w.bx + w.dragDx, by = w.by + w.dragDy;
    ctx.save();
    ctx.globalAlpha = (selected && !w.selected) ? 0.18 : 1;
    ctx.font = `bold ${w.fs}px Arial`;
    ctx.fillStyle = w.color;

    if (w.angle === 0) {
      if (w.selected) {
        ctx.save(); ctx.fillStyle='rgba(0,0,0,0.08)';
        ctx.fillRect(bx-2, by-2, w.bw+4, w.bh+4); ctx.restore();
      }
      ctx.fillText(w.word, bx, by + w.fs * 0.88);
    } else {
      const bcx = bx+w.bw/2, bcy = by+w.bh/2;
      if (w.selected) {
        ctx.save(); ctx.fillStyle='rgba(0,0,0,0.08)';
        ctx.fillRect(bx-2, by-2, w.bw+4, w.bh+4); ctx.restore();
      }
      ctx.translate(bcx, bcy); ctx.rotate(-Math.PI/2);
      ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(w.word, 0, 0);
    }

    if (w.selected) {
      ctx.restore(); ctx.save();
      ctx.globalAlpha=1; ctx.strokeStyle=w.color;
      ctx.lineWidth=1.5/zoom; ctx.setLineDash([4/zoom, 3/zoom]);
      ctx.strokeRect(bx-3, by-3, w.bw+6, w.bh+6);
    }
    ctx.restore();
  }
  ctx.restore();
}

// ── Hit test ───────────────────────────────────────────────────────────────
const toWorld = (cx,cy) => ({ x:(cx-panX)/zoom, y:(cy-panY)/zoom });

function hitTest(cx, cy) {
  const {x,y} = toWorld(cx,cy);
  for (let i=words.length-1; i>=0; i--) {
    const w=words[i], bx=w.bx+w.dragDx, by=w.by+w.dragDy;
    if (x>=bx-4&&x<=bx+w.bw+4&&y>=by-4&&y<=by+w.bh+4) return w;
  }
  return null;
}

// ── Mouse ──────────────────────────────────────────────────────────────────
canvas.addEventListener('mousedown', e => {
  const r=canvas.getBoundingClientRect();
  const cx=e.clientX-r.left, cy=e.clientY-r.top;
  mdX=cx; mdY=cy; didMove=false;
  const hit=hitTest(cx,cy);
  if (hit) {
    draggingWord=hit;
    const wp=toWorld(cx,cy);
    wdOfsX=wp.x-hit.dragDx-hit.bx; wdOfsY=wp.y-hit.dragDy-hit.by;
  } else {
    draggingCanvas=true; dragCvX=e.clientX; dragCvY=e.clientY; panSX=panX; panSY=panY;
  }
  wrap.classList.add('dragging');
});

window.addEventListener('mousemove', e => {
  const r=canvas.getBoundingClientRect();
  const cx=e.clientX-r.left, cy=e.clientY-r.top;
  if (Math.abs(cx-mdX)>3||Math.abs(cy-mdY)>3) didMove=true;

  if (draggingWord) {
    const wp=toWorld(cx,cy);
    draggingWord.dragDx=wp.x-wdOfsX-draggingWord.bx;
    draggingWord.dragDy=wp.y-wdOfsY-draggingWord.by;
    draw(); return;
  }
  if (draggingCanvas) {
    panX=panSX+(e.clientX-dragCvX); panY=panSY+(e.clientY-dragCvY); draw(); return;
  }

  const hit=hitTest(cx,cy);
  if (hit!==hovered) {
    if (hovered) hovered.hovered=false;
    hovered=hit; if (hovered) hovered.hovered=true; draw();
  }

  const tt=document.getElementById('tooltip');
  if (hit) {
    wrap.style.cursor='pointer';
    document.getElementById('tt-word').textContent=hit.word;
    const tr=lang==='fr'?`  →  ${FR_TRANSLATIONS[hit.word]||'?'}`:'';
    // TF = raw count; TF-IDF = TF * log(N/Df)
    document.getElementById('tt-info').textContent=
      `tf: ${hit.tf}   idf: ${hit.idf != null ? hit.idf.toFixed(5) : '—'}   tf-idf: ${hit.tfidf != null ? hit.tfidf.toFixed(5) : '—'}${tr}`;
    tt.style.left=(e.clientX+14)+'px'; tt.style.top=(e.clientY-8)+'px';
    tt.classList.add('show');
  } else {
    wrap.style.cursor='grab'; tt.classList.remove('show');
  }
});

window.addEventListener('mouseup', e => {
  const r = canvas.getBoundingClientRect();
  const cx = e.clientX - r.left, cy = e.clientY - r.top;
  const hit = hitTest(cx, cy);
  draggingWord = null;
  draggingCanvas = false;
  wrap.classList.remove('dragging');
  if (hit) {
    selectWord(hit);
  } else {
    deselect();
  }
});

canvas.addEventListener('mouseleave', () => {
  document.getElementById('tooltip').classList.remove('show');
  if (hovered) { hovered.hovered=false; hovered=null; draw(); }
});

canvas.addEventListener('wheel', e => {
  e.preventDefault();
  const r=canvas.getBoundingClientRect();
  const mx=e.clientX-r.left, my=e.clientY-r.top;
  const nz=Math.max(0.2,Math.min(5,zoom+(e.deltaY<0?0.12:-0.12)));
  panX=mx-(mx-panX)*(nz/zoom); panY=my-(my-panY)*(nz/zoom);
  zoom=nz; updateZoomLabel(); draw();
}, {passive:false});

canvas.addEventListener('dblclick', ()=>{ deselect(); resetView(); });

// ── Selection ──────────────────────────────────────────────────────────────
function selectWord(w) {
  if (selected) selected.selected=false;
  selected=w; w.selected=true; draw(); showCard(w); highlightList(w.word);
}

function deselect() {
  if (selected) selected.selected=false; selected=null; draw();
  document.getElementById('word-card').className='empty';
  document.getElementById('card-hint').style.display='';
  document.getElementById('card-word').style.display='none';
  document.getElementById('card-stats').style.display='none';
  document.getElementById('card-translation').textContent='';
  highlightList(null);
}

function showCard(w) {
  document.getElementById('word-card').className='';
  document.getElementById('card-hint').style.display='none';
  const wEl=document.getElementById('card-word');
  wEl.style.display=''; wEl.textContent=w.word; wEl.style.color=w.color;
  const maxC=DATA[lang][0].count, pct=Math.round(w.count/maxC*100);
  document.getElementById('card-translation').textContent=
    lang==='fr'?'→ '+(FR_TRANSLATIONS[w.word]||'(no translation)'):'';
  // TF = raw count; IDF = log(N/Df); TF-IDF = TF * IDF
  document.getElementById('s-rank').textContent='#'+w.rank;
  document.getElementById('s-tf').textContent=w.tf;
  document.getElementById('s-idf').textContent=w.idf != null ? w.idf.toFixed(5) : '—';
  document.getElementById('s-tfidf').textContent=w.tfidf != null ? w.tfidf.toFixed(5) : '—';
  document.getElementById('s-pct').textContent=pct+'% of top term';
  document.getElementById('tf-bar').style.width=pct+'%';
  document.getElementById('tf-bar').style.background=w.color;
  document.getElementById('card-stats').style.display='';
}

// ── Word list ──────────────────────────────────────────────────────────────
function buildList() {
  const data=DATA[lang], isFr=lang==='fr';
  document.getElementById('word-list').innerHTML=data.slice(0,30).map((item,i)=>{
    const color=getColor(i);
    const tr=isFr&&FR_TRANSLATIONS[item.word]?FR_TRANSLATIONS[item.word]:'';
    return `<div class="list-row" data-word="${item.word}" onclick="listClick('${item.word}')">
      <span class="list-rank">${i+1}</span>
      <span class="list-word" style="color:${color}">${item.word}</span>
      ${tr?`<span class="list-tr">${tr}</span>`:''}
      <span class="list-count">${item.count}</span>
    </div>`;
  }).join('');
}

function listClick(word) {
  const w=words.find(x=>x.word===word); if(!w) return;
  selectWord(w);
  smoothPan(canvas.width/2-(w.bx+w.dragDx+w.bw/2)*zoom,
            canvas.height/2-(w.by+w.dragDy+w.bh/2)*zoom);
}

function highlightList(word) {
  document.querySelectorAll('.list-row').forEach(el=>
    el.classList.toggle('active', el.dataset.word===word));
}

function smoothPan(tx,ty) {
  const sx=panX,sy=panY,t0=performance.now();
  (function step(t){
    const p=Math.min(1,(t-t0)/320), e=p<.5?2*p*p:-1+(4-2*p)*p;
    panX=sx+(tx-sx)*e; panY=sy+(ty-sy)*e; draw();
    if(p<1) requestAnimationFrame(step);
  })(t0);
}

// ── Controls ───────────────────────────────────────────────────────────────
function doZoom(dz) {
  const cx=canvas.width/2,cy=canvas.height/2,nz=Math.max(0.2,Math.min(5,zoom+dz));
  panX=cx-(cx-panX)*(nz/zoom); panY=cy-(cy-panY)*(nz/zoom);
  zoom=nz; updateZoomLabel(); draw();
}
function updateZoomLabel() { document.getElementById('zoom-label').textContent=Math.round(zoom*100)+'%'; }
function resetView() { zoom=1; panX=0; panY=0; updateZoomLabel(); draw(); }

function switchLang(l) {
  lang=l; selected=null; hovered=null;
  document.getElementById('btn-en').className='tab-btn'+(l==='en'?' active':'');
  document.getElementById('btn-fr').className='tab-btn'+(l==='fr'?' active':'');
  resetView(); init();
}

// ── Init ───────────────────────────────────────────────────────────────────
function resize() { canvas.width=wrap.clientWidth; canvas.height=wrap.clientHeight; }
function init()   { resize(); layout(); buildList(); deselect(); draw(); }
window.addEventListener('resize', ()=>{ if(DATA) init(); });

// Entry point — waits for the JSON
loadData();