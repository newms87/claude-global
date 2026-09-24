import json

# ============================================================================
# Tabbed tracker artifact — reusable template
#
# A self-contained, data-driven HTML/CSS/JS "living tracker" page: tabs with
# live counts, a search box that filters every field, light/dark theme,
# and three card shapes (Open / Decided / Run-log). Card anatomy is the
# whole point of this template — see the usage notes in the companion
# README.md before filling in real data. Short version:
#
#   - Everything actionable goes at the TOP of the card, uncollapsed:
#     a numbered "needs" list (steps for the human) and/or "solutions"
#     (named options, each with a collapsible pros/cons breakdown).
#   - "context" is background/problem-statement ONLY, and stays collapsed
#     by default under a "Background" toggle. If it's something the reader
#     must act on or decide, it does NOT belong in context — see needs/
#     solutions/resolution instead.
#
# Fill in PROJECT + OUT below, replace the EXAMPLE entries in OPEN / PLAN /
# DECIDED / RUNS with real data, then:  python3 build.py
# Everything below the data section (CSS + JS engine) is generic — you
# should not need to touch it for a normal tracker. If you do change it,
# consider syncing the fix back to this template so the next repo gets it.
# ============================================================================

OUT = "/tmp/tracker.html"  # <-- point this at your session scratchpad path

NOW = "YYYY-MM-DD HH:MM TZ"  # <-- update this every time you rebuild

PROJECT = {
  "name": "Project Tracker",       # short, distinctive — becomes the <h1> and artifact title
  "sub": "repo-or-topic · living tracker",  # short static prefix for the footer subtitle line
  "logo": "PT",                    # 1-2 characters shown in the little logo badge
}

# ============================================================================
# OPEN — things that need the human's input or action right now. Each entry:
#   ref        stable id, e.g. "BUILD-CACHE" — NEVER renumber once assigned
#   ts         "YYYY-MM-DD HH:MM TZ" — real clock time, updated whenever touched
#   title      one line
#   status     optional: "mine" (you're driving it) | "needs_input" (default) | "backlog"
#   needsLabel optional override for the needs-list heading (default "What I need from you")
#   needs      optional array of short, numbered, ACTIONABLE strings — the steps/asks
#              themselves, rendered visibly at the top of the card, no click required
#   solutions  optional array of {title, pros[], cons[], recommended?} — named options
#              with a collapsible pros/cons breakdown, also rendered at the top
#   context    background/problem-statement prose — collapsed by default under
#              "Background". Never put an action item or a decision the reader must
#              make in here; if it's actionable, it belongs in needs or solutions.
# ============================================================================
OPEN = [
  {
    "ref": "EXAMPLE-NEEDS",
    "ts": "2026-01-01 00:00 UTC",
    "title": "EXAMPLE — an ask with a short numbered checklist for the human",
    "status": "needs_input",
    "needsLabel": "What I need from you",
    "needs": [
      "Short, concrete, actionable — the first thing the reader should do.",
      "Each item stands alone; the reader should be able to act on #2 without reading #1.",
    ],
    "context": "Background ONLY: why this came up, what was already tried, caveats. This text is collapsed by default — nothing the reader must act on should live only here.",
    "solutions": [],
  },
  {
    "ref": "EXAMPLE-SOLUTIONS",
    "ts": "2026-01-01 00:00 UTC",
    "title": "EXAMPLE — a decision between named options, each with tradeoffs",
    "status": "needs_input",
    "context": "Background on why a decision is needed here, and what happens under each option at a mechanical level. Still collapsed by default.",
    "solutions": [
      {
        "title": "A. The recommended option (RECOMMENDED)",
        "recommended": True,
        "pros": ["Why this is the safer/cheaper/faster choice."],
        "cons": ["The real cost or risk it still carries."],
      },
      {
        "title": "B. The alternative",
        "pros": ["What it buys you instead."],
        "cons": ["Why it is not the default."],
      },
    ],
  },
]

# ============================================================================
# PLAN — your own queued next steps (same card shape as OPEN, status usually "mine").
# ============================================================================
PLAN = [
  {
    "ref": "EXAMPLE-PLAN",
    "ts": "2026-01-01 00:00 UTC",
    "status": "mine",
    "title": "EXAMPLE — next thing you intend to do, not waiting on the human",
    "needs": [],
    "context": "Why this is next, what it depends on.",
    "solutions": [],
  },
]

# ============================================================================
# DECIDED — the settled archive. Same needs/solutions-at-top-level principle,
# plus "resolution" (what actually happened / what was decided — also
# uncollapsed) and "verdict": "accepted" | "rejected" | "caveat".
# ============================================================================
DECIDED = [
  {
    "ref": "EXAMPLE-DECIDED",
    "ts": "2026-01-01 00:00 UTC",
    "verdict": "accepted",
    "title": "EXAMPLE — a settled decision, archived so it is never re-litigated",
    "context": "Why this came up — background only, collapsed by default.",
    "resolution": "What was decided or found, and the evidence for it. Shown at top level, uncollapsed — this is the part a reader actually needs.",
  },
]

# ============================================================================
# RUNS — a chronological log (test runs, deploys, experiments...). Rendered
# as compact rows, newest first (sorted by ts at build time), not full cards.
# ============================================================================
RUNS = [
  {
    "ref": "RUN-1", "ts": "2026-01-01 00:00 UTC", "what": "EXAMPLE — one line naming the run",
    "config": "e.g. model/flags used", "result": "pass",  # pass | fail | stopped | pending
    "score": "one-line verdict", "timing": "wall-clock", "spend": "cost, if relevant",
    "notes": "What happened, with real numbers. This is the only free-text field on a run row.",
  },
]

def esc(s):
    return (str(s) if s is not None else "")

HTML = r"""<style>
  :root{
    color-scheme: light;
    --page:#f9f9f7; --surface:#fcfcfb; --surface-2:#f4f3ef; --surface-3:#eceae4;
    --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
    --grid:#e1e0d9; --axis:#b9b7ad; --border:rgba(11,11,11,0.10);
    --brand:#0f7368; --brand-strong:#0a4f47; --brand-soft:#cbe8e3;
    --good:#0ca30c; --warn:#c98500; --crit:#d03b3b;
    --radius-sm:10px;
    --shadow:0 1px 2px rgba(11,11,11,0.04),0 6px 20px rgba(11,11,11,0.05);
    --mono:"SF Mono",ui-monospace,"Cascadia Code","JetBrains Mono",Menlo,Consolas,monospace;
    --sans:system-ui,-apple-system,"Segoe UI",sans-serif;
    --badge-good-bg:#d6f2d6; --badge-good-fg:#0a5c0a;
    --badge-bad-bg:#ffd9d9; --badge-bad-fg:#8f1f1f;
    --badge-warn-bg:#fff3d6; --badge-warn-fg:#7a5a00;
    --mark-bg:#ffe9a8;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]){
      color-scheme: dark;
      --page:#0d0d0d; --surface:#1a1a19; --surface-2:#232322; --surface-3:#2c2c2a;
      --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
      --grid:#2c2c2a; --axis:#4a4a46; --border:rgba(255,255,255,0.12);
      --brand:#3fb3a4; --brand-strong:#8ad5c9; --brand-soft:#123430;
      --good:#0ca30c; --warn:#c98500; --crit:#e66767;
      --shadow:0 1px 2px rgba(0,0,0,0.4),0 8px 26px rgba(0,0,0,0.5);
      --badge-good-bg:#0f3a1a; --badge-good-fg:#8fd9a0;
      --badge-bad-bg:#4a1414; --badge-bad-fg:#f0a0a0;
      --badge-warn-bg:#3d2f0a; --badge-warn-fg:#e0c477;
      --mark-bg:#5c4a14;
    }
  }
  :root[data-theme="dark"]{
    color-scheme: dark;
    --page:#0d0d0d; --surface:#1a1a19; --surface-2:#232322; --surface-3:#2c2c2a;
    --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --axis:#4a4a46; --border:rgba(255,255,255,0.12);
    --brand:#3fb3a4; --brand-strong:#8ad5c9; --brand-soft:#123430;
    --good:#0ca30c; --warn:#c98500; --crit:#e66767;
    --shadow:0 1px 2px rgba(0,0,0,0.4),0 8px 26px rgba(0,0,0,0.5);
    --badge-good-bg:#0f3a1a; --badge-good-fg:#8fd9a0;
    --badge-bad-bg:#4a1414; --badge-bad-fg:#f0a0a0;
    --badge-warn-bg:#3d2f0a; --badge-warn-fg:#e0c477;
    --mark-bg:#5c4a14;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--page);color:var(--ink);font-family:var(--sans);
    font-size:15.5px;line-height:1.6;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1100px;margin:0 auto;padding:0 clamp(16px,3vw,32px) 90px}
  header.top{padding:28px 0 0}
  .titlebar{display:flex;align-items:flex-start;gap:14px;flex-wrap:wrap}
  .logo{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--brand),var(--brand-strong));
    display:grid;place-items:center;color:#fff;font-weight:800;font-size:16px;flex:none}
  h1{font-size:24px;margin:0;letter-spacing:-.02em;font-weight:800;line-height:1.2}
  .sub{color:var(--muted);font-size:13px;margin-top:3px}
  .spacer{flex:1}
  .toggle{display:flex;gap:4px;background:var(--surface-2);padding:3px;border-radius:9px;border:1px solid var(--border)}
  .toggle button{border:0;background:transparent;color:var(--ink-2);font:inherit;font-size:12px;
    padding:5px 11px;border-radius:6px;cursor:pointer}
  .toggle button.on{background:var(--surface);color:var(--ink);box-shadow:var(--shadow);font-weight:600}
  .tabs{display:flex;gap:4px;margin:22px 0 0;border-bottom:1px solid var(--border)}
  .tabs button{border:0;background:transparent;font:inherit;font-size:15px;color:var(--ink-2);
    padding:11px 18px;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;
    display:flex;align-items:center;gap:8px;border-radius:8px 8px 0 0;font-weight:600}
  .tabs button:hover{background:var(--surface-2);color:var(--ink)}
  .tabs button.on{color:var(--brand);border-bottom-color:var(--brand)}
  .tabs .cnt{background:var(--surface-3);color:var(--ink-2);font-size:11.5px;font-weight:700;
    padding:1px 8px;border-radius:999px;font-variant-numeric:tabular-nums}
  .tabs button.on .cnt{background:var(--brand);color:#fff}
  .search{margin:16px 0 4px;position:relative}
  .search input{width:100%;padding:9px 13px 9px 34px;border-radius:9px;border:1px solid var(--border);
    background:var(--surface);color:var(--ink);font:inherit;font-size:14px}
  .search .ico{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:14px}
  .panel{display:none;padding-top:8px}
  .panel.on{display:block}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);
    padding:16px 18px;margin:11px 0;box-shadow:var(--shadow)}
  .card-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .ref{font-family:var(--mono);font-size:11.5px;font-weight:700;color:var(--brand);
    background:var(--brand-soft);padding:2px 8px;border-radius:6px;letter-spacing:.02em;flex:none}
  .card h3{margin:8px 0 0;font-size:15.5px;font-weight:700;letter-spacing:-.01em;line-height:1.4}
  .ts{font-family:var(--mono);font-size:10.5px;color:var(--muted);white-space:nowrap;margin-left:auto}
  .verdict{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
    padding:2px 8px;border-radius:999px;flex:none}
  .v-accepted{background:var(--badge-good-bg);color:var(--badge-good-fg)}
  .v-rejected{background:var(--badge-bad-bg);color:var(--badge-bad-fg)}
  .v-caveat{background:var(--badge-warn-bg);color:var(--badge-warn-fg)}
  .s-mine{background:var(--brand-soft);color:var(--brand-strong)}
  .s-needs_input{background:var(--badge-bad-bg);color:var(--badge-bad-fg)}
  .s-backlog{background:var(--surface-3);color:var(--muted)}
  details.ctx{margin-top:10px;border:1px solid var(--border);border-radius:8px;background:var(--surface-2)}
  details.ctx summary{cursor:pointer;padding:8px 12px;font-size:12px;font-weight:700;color:var(--ink-2);
    letter-spacing:.03em;text-transform:uppercase;list-style:none;display:flex;align-items:center;gap:6px}
  details.ctx summary::-webkit-details-marker{display:none}
  details.ctx summary::before{content:"▸";display:inline-block;transition:transform .15s;color:var(--muted)}
  details.ctx[open] summary::before{transform:rotate(90deg)}
  details.ctx .body{padding:2px 14px 12px;font-size:14px;color:var(--ink-2);white-space:pre-wrap}
  .resolution{margin-top:10px;padding:11px 14px;border-radius:8px;background:var(--surface-2);
    border:1px solid var(--border);font-size:14px;color:var(--ink-2);white-space:pre-wrap}
  .resolution .rk{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
    color:var(--good);margin-bottom:5px;display:block}
  .needs{margin-top:10px;padding:12px 15px;border-radius:8px;background:var(--brand-soft);
    border:1px solid var(--border)}
  .needs .nk{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
    color:var(--brand-strong);margin-bottom:7px;display:block;font-weight:700}
  .needs ol{margin:0;padding-left:19px;display:flex;flex-direction:column;gap:7px}
  .needs li{font-size:14px;color:var(--ink);line-height:1.5}
  .sols{margin-top:12px;display:flex;flex-direction:column;gap:8px}
  .sol{border:1px solid var(--border);border-radius:8px;overflow:hidden}
  .sol-head{padding:9px 13px;font-size:13.5px;font-weight:600;background:var(--surface-2);
    display:flex;align-items:center;gap:8px}
  .sol.rec .sol-head{background:var(--brand-soft);color:var(--brand-strong)}
  .rec-flag{font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;
    color:#fff;background:var(--good);border-radius:3px;padding:2px 6px;margin-left:auto;flex:none}
  details.pc summary{cursor:pointer;padding:7px 13px;font-size:11.5px;color:var(--muted);
    list-style:none;display:flex;align-items:center;gap:5px}
  details.pc summary::-webkit-details-marker{display:none}
  details.pc summary::before{content:"▸";display:inline-block;transition:transform .15s}
  details.pc[open] summary::before{transform:rotate(90deg)}
  .pc-body{padding:0 13px 12px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
  @media(max-width:560px){.pc-body{grid-template-columns:1fr}}
  .pc-col h5{margin:0 0 6px;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
  .pc-col.pro h5{color:var(--good)}
  .pc-col.con h5{color:var(--crit)}
  .pc-col ul{margin:0;padding-left:16px;font-size:13px;color:var(--ink-2)}
  .pc-col li{margin:3px 0}
  .run{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);
    padding:13px 16px;margin:9px 0;box-shadow:var(--shadow)}
  .run-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .run h4{margin:7px 0 0;font-size:14.5px;font-weight:700;line-height:1.4}
  .r-pass{background:var(--badge-good-bg);color:var(--badge-good-fg)}
  .r-fail{background:var(--badge-bad-bg);color:var(--badge-bad-fg)}
  .r-pending{background:var(--badge-warn-bg);color:var(--badge-warn-fg)}
  .r-stopped{background:var(--surface-3);color:var(--muted)}
  .run-meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:9px;font-size:12.5px;color:var(--ink-2)}
  .run-meta b{font-family:var(--mono);font-size:11px;color:var(--muted);font-weight:700;
    letter-spacing:.04em;text-transform:uppercase;display:block}
  .run-notes{margin-top:9px;font-size:13.5px;color:var(--ink-2);line-height:1.55}
  .empty{color:var(--muted);font-size:14px;padding:30px 0;text-align:center}
  .foot{margin-top:32px;padding-top:16px;border-top:1px solid var(--border);color:var(--muted);font-size:12.5px}
  mark{background:var(--mark-bg);color:inherit;padding:0 1px;border-radius:2px}
</style>
<div class="wrap">
  <header class="top">
    <div class="titlebar">
      <div class="logo">""" + esc(PROJECT["logo"]) + r"""</div>
      <div>
        <h1>""" + esc(PROJECT["name"]) + r"""</h1>
        <div class="sub" id="sub"></div>
      </div>
      <div class="spacer"></div>
      <div class="toggle" role="group" aria-label="Theme">
        <button data-t="light">Light</button>
        <button data-t="dark">Dark</button>
      </div>
    </div>
  </header>
  <nav class="tabs" id="tabs"></nav>
  <div class="search"><span class="ico">⌕</span><input type="text" id="q" placeholder="Search…"></div>
  <main id="panels"></main>
  <div class="foot">Updated after every action taken or new information received — this page, not the chat, is the record.</div>
</div>
<script>
const NOW = """ + json.dumps(NOW) + r""";
const PROJECT_SUB = """ + json.dumps(PROJECT["sub"]) + r""";
const OPEN = """ + json.dumps(OPEN, indent=None) + r""";
const DECIDED = """ + json.dumps(DECIDED, indent=None) + r""";
const PLAN = """ + json.dumps(PLAN, indent=None) + r""";
const RUNS = """ + json.dumps(sorted(RUNS, key=lambda r: r["ts"], reverse=True), indent=None) + r"""

document.getElementById("sub").textContent =
  PROJECT_SUB + " · " + NOW + " · " + OPEN.length + " open · " + PLAN.length + " planned · " + DECIDED.length + " decided · " + RUNS.length + " runs";

document.querySelectorAll(".toggle button").forEach((b) => {
  b.addEventListener("click", () => {
    document.documentElement.setAttribute("data-theme", b.dataset.t);
    document.querySelectorAll(".toggle button").forEach((x) => x.classList.toggle("on", x === b));
  });
});

// Sync the toggle's visual .on state to whatever theme actually applied on
// load (an explicit host data-theme attribute, else the OS/system
// preference) — WITHOUT stamping data-theme ourselves, so a reader who
// never clicks keeps following live OS theme changes.
(() => {
  const explicit = document.documentElement.getAttribute("data-theme");
  const effective = explicit || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.querySelectorAll(".toggle button").forEach((b) => b.classList.toggle("on", b.dataset.t === effective));
})();

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function mark(s, term) {
  const e = esc(s);
  if (!term) return e;
  const rx = new RegExp("(" + term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
  return e.replace(rx, "<mark>$1</mark>");
}
function nl2br(s, term) {
  return mark(s, term).replace(/\n/g, "<br>");
}

let active = "open";
let query = "";

function buildTabs() {
  const $tabs = document.getElementById("tabs");
  $tabs.innerHTML = "";
  [["open", "Open", OPEN], ["plan", "Plan", PLAN], ["decided", "Decided", DECIDED], ["runs", "Runs", RUNS]].forEach(([key, label, list]) => {
    const b = document.createElement("button");
    b.className = key === active ? "on" : "";
    b.innerHTML = label + ' <span class="cnt">' + list.length + "</span>";
    b.addEventListener("click", () => { active = key; render(); });
    $tabs.appendChild(b);
  });
}

function matches(item, term) {
  if (!term) return true;
  return JSON.stringify(item).toLowerCase().indexOf(term.toLowerCase()) > -1;
}

function renderSolution(sol, term) {
  const cls = sol.recommended ? "sol rec" : "sol";
  const pros = (sol.pros || []).map((p) => "<li>" + mark(p, term) + "</li>").join("");
  const cons = (sol.cons || []).map((c) => "<li>" + mark(c, term) + "</li>").join("");
  return (
    '<div class="' + cls + '">' +
      '<div class="sol-head">' + mark(sol.title, term) +
        (sol.recommended ? '<span class="rec-flag">Recommended</span>' : "") +
      "</div>" +
      '<details class="pc"><summary>pros / cons</summary>' +
        '<div class="pc-body">' +
          '<div class="pc-col pro"><h5>Pros</h5><ul>' + (pros || "<li>—</li>") + "</ul></div>" +
          '<div class="pc-col con"><h5>Cons</h5><ul>' + (cons || "<li>—</li>") + "</ul></div>" +
        "</div>" +
      "</details>" +
    "</div>"
  );
}

const STATUS_LABEL = { mine: "Next up", needs_input: "Needs your call", backlog: "Backlog" };

function renderNeeds(item, term) {
  if (!item.needs || !item.needs.length) return "";
  const label = item.needsLabel || "What I need from you";
  const li = item.needs.map((n) => "<li>" + mark(n, term) + "</li>").join("");
  return '<div class="needs"><span class="nk">' + esc(label) + "</span><ol>" + li + "</ol></div>";
}

function renderOpenCard(item, term) {
  const sols = (item.solutions || []).map((s) => renderSolution(s, term)).join("");
  const statusCls = "s-" + (item.status || "needs_input");
  const statusLabel = STATUS_LABEL[item.status] || STATUS_LABEL.needs_input;
  return (
    '<div class="card">' +
      '<div class="card-head">' +
        '<span class="ref">' + esc(item.ref) + "</span>" +
        '<span class="verdict ' + statusCls + '">' + esc(statusLabel) + "</span>" +
        '<span class="ts">' + esc(item.ts) + "</span>" +
      "</div>" +
      "<h3>" + mark(item.title, term) + "</h3>" +
      renderNeeds(item, term) +
      (sols ? '<div class="sols">' + sols + "</div>" : "") +
      '<details class="ctx"><summary>Background</summary><div class="body">' + nl2br(item.context, term) + "</div></details>" +
    "</div>"
  );
}

function renderDecidedCard(item, term) {
  const vcls = { accepted: "v-accepted", rejected: "v-rejected", caveat: "v-caveat" }[item.verdict] || "v-caveat";
  const sols = (item.solutions || []).map((s) => renderSolution(s, term)).join("");
  return (
    '<div class="card">' +
      '<div class="card-head">' +
        '<span class="ref">' + esc(item.ref) + "</span>" +
        '<span class="verdict ' + vcls + '">' + esc(item.verdict) + "</span>" +
        '<span class="ts">' + esc(item.ts) + "</span>" +
      "</div>" +
      "<h3>" + mark(item.title, term) + "</h3>" +
      renderNeeds(item, term) +
      (sols ? '<div class="sols">' + sols + "</div>" : "") +
      (item.resolution ? '<div class="resolution"><span class="rk">Resolution</span>' + nl2br(item.resolution, term) + "</div>" : "") +
      '<details class="ctx"><summary>Background</summary><div class="body">' + nl2br(item.context, term) + "</div></details>" +
    "</div>"
  );
}

function renderRun(item, term) {
  const cls = "r-" + (item.result || "stopped");
  return (
    '<div class="run">' +
      '<div class="run-head">' +
        '<span class="ref">' + esc(item.ref) + "</span>" +
        '<span class="verdict ' + cls + '">' + esc(item.result) + "</span>" +
        '<span class="ts">' + esc(item.ts) + "</span>" +
      "</div>" +
      "<h4>" + mark(item.what, term) + "</h4>" +
      '<div class="run-meta">' +
        "<span><b>Result</b>" + mark(item.score, term) + "</span>" +
        "<span><b>Config</b>" + mark(item.config, term) + "</span>" +
        "<span><b>Timing</b>" + mark(item.timing, term) + "</span>" +
        "<span><b>Spend</b>" + mark(item.spend, term) + "</span>" +
      "</div>" +
      '<div class="run-notes">' + mark(item.notes, term) + "</div>" +
    "</div>"
  );
}

function render() {
  buildTabs();
  const source = active === "open" ? OPEN : active === "plan" ? PLAN
    : active === "decided" ? DECIDED : RUNS;
  const list = source.filter((i) => matches(i, query));
  const $panels = document.getElementById("panels");
  if (!list.length) {
    $panels.innerHTML = '<p class="empty">Nothing here.</p>';
    return;
  }
  const renderer = active === "runs" ? renderRun
    : active === "decided" ? renderDecidedCard : renderOpenCard;
  const html = list.map((i) => renderer(i, query)).join("");
  $panels.innerHTML = '<section class="panel on">' + html + "</section>";
}

document.getElementById("q").addEventListener("input", (e) => {
  query = e.target.value.trim();
  render();
});

render();
</script>

"""

open(OUT, "w").write(HTML)
print("OK bytes:", len(HTML), "| OPEN:", len(OPEN), "| DECIDED:", len(DECIDED))
