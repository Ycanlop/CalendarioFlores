#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generar_paginas.py — Regenera flores.js, dias.html y las 365 páginas
dia-MM-DD.html (con desbloqueo día a día) a partir de flores.json.

Uso:  python generar_paginas.py
"""
import json, re, unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
         "septiembre","octubre","noviembre","diciembre"]

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def load():
    entries = json.loads((BASE / "flores.json").read_text(encoding="utf-8"))
    for e in entries:
        e["slug"] = slugify(e["name"])
        e["key"] = e["mm"] + "-" + e["dd"]
        e["year"] = 2026 if (int(e["mm"]), int(e["dd"])) >= (9, 29) else 2027
        e["fdate"] = "%d de %s de %d" % (int(e["dd"]), MESES[int(e["mm"]) - 1], e["year"])
        e["fshort"] = "%d %s." % (int(e["dd"]), MESES[int(e["mm"]) - 1][:3])
    return entries

# ---------- flores.js (datos para las páginas) ----------
def build_js(entries):
    data = [{"n": e["n"], "key": e["key"], "mm": e["mm"], "dd": e["dd"],
             "slug": e["slug"], "name": e["name"], "meaning": e["meaning"],
             "year": e["year"], "fdate": e["fdate"], "fshort": e["fshort"]}
            for e in entries]
    return ("/* Datos del calendario — generado desde flores.json. "
            "No edites a mano. */\nconst FLORES = "
            + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")

# ---------- Plantilla de cada día (con candado si es futuro) ----------
DAY = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flor del día — 365 Días, 365 Flores 🌸</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <a class="btn btn-ghost" href="index.html">← Inicio</a>
  <span class="topbar-date">🌸 Calendario floral</span>
  <a class="btn btn-ghost" href="dias.html">📅 Todos los días</a>
</header>
<main class="day" id="main"></main>
<script src="flores.js"></script>
<script>
(function () {
  var KEY = '@@KEY@@';
  var e = null, idx = -1;
  for (var i = 0; i < FLORES.length; i++) {
    if (FLORES[i].key === KEY) { e = FLORES[i]; idx = i; break; }
  }
  var main = document.getElementById('main');
  if (!e) { main.innerHTML = '<p>Día no encontrado 🥀</p>'; return; }

  var now = new Date();
  var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  function unlockDate(d) {
    return new Date(d.year, parseInt(d.mm, 10) - 1, parseInt(d.dd, 10));
  }
  var prev = FLORES[idx - 1], next = FLORES[idx + 1];

  function nav() {
    var h = '<nav class="daynav">';
    if (prev) {
      h += (today >= unlockDate(prev))
        ? '<a class="btn" href="dia-' + prev.key + '.html">← ' + prev.fshort + ': ' + prev.name + '</a>'
        : '<a class="btn" href="dia-' + prev.key + '.html">← Día anterior 🔒</a>';
    } else { h += '<span></span>'; }
    if (next) {
      h += (today >= unlockDate(next))
        ? '<a class="btn" href="dia-' + next.key + '.html">' + next.name + ': ' + next.fshort + ' →</a>'
        : '<a class="btn" href="dia-' + next.key + '.html">Día siguiente 🔒 →</a>';
    } else { h += '<span></span>'; }
    return h + '</nav>';
  }

  if (today >= unlockDate(e)) {
    /* ---------- DÍA DESBLOQUEADO ---------- */
    document.title = e.fdate + ' · ' + e.name + ' — 365 Días, 365 Flores 🌸';
    main.innerHTML =
      '<p class="kicker">Flor n.º ' + e.n + ' del calendario · ' + e.fdate + '</p>' +
      '<h1>' + e.name + '</h1>' +
      '<p class="meaning">«' + e.meaning + '»</p>' +
      '<figure class="photo"><img src="img/' + e.key + '-' + e.slug + '.jpg" alt="' + e.name + '" loading="lazy" ' +
      'onerror="this.onerror=null;this.src=\'https://placehold.co/1000x700/f3e5f5/6a4c76?text=' + e.slug.replace(/-/g, '+') + '\'">' +
      '<figcaption>Sustituye esta imagen por tu foto: <code>img/' + e.key + '-' + e.slug + '.jpg</code></figcaption></figure>' +
      '<p class="desc">Hoy, <strong>' + e.fdate + '</strong>, la flor del día es el <strong>' + e.name + '</strong>, ' +
      'que en este calendario simboliza <strong>«' + e.meaning + '»</strong>. ' +
      'Un día, una flor, un mensaje: guarda este pequeño ritual floral contigo. 🌸</p>' +
      nav();
  } else {
    /* ---------- DÍA BLOQUEADO ---------- */
    var dias = Math.round((unlockDate(e) - today) / 864e5);
    document.title = '🔒 Flor del ' + e.fdate + ' — aún bloqueada';
    main.innerHTML =
      '<p class="lock-emoji">🔒</p>' +
      '<h1>Una flor misteriosa</h1>' +
      '<p class="meaning">Se desbloquea el ' + e.fdate + '</p>' +
      '<figure class="photo"><img src="https://placehold.co/1000x700/efe6f0/8a6a92?text=%3F" alt="Flor misteriosa"></figure>' +
      '<p class="desc">Esta flor aún está en el capullo 🌱. Vuelve en <strong>' + dias + ' día' +
      (dias === 1 ? '' : 's') + '</strong> para descubrirla.<br>' +
      'Pista: su nombre empieza por «<strong>' + e.name.charAt(0).toUpperCase() + '</strong>»…</p>' +
      nav();
  }
})();
</script>
</body>
</html>
"""

# ---------- dias.html (selector con candados y progreso) ----------
DIAS = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Todos los días — 365 Días, 365 Flores 🌸</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <a class="btn btn-ghost" href="index.html">← Inicio</a>
  <span class="topbar-date">🌸 365 días</span>
  <a class="btn btn-ghost" href="dia_actual.html">📅 Día actual</a>
</header>
<main class="picker">
  <h1>Elige tu día 🌼</h1>
  <p>Del 29/09/2026 al 28/09/2027 · cada día se desbloquea a las 00:00 de su fecha.</p>
  <p id="prog" class="prog"></p>
  <div class="progress"><div id="bar"></div></div>
  <input id="q" class="search" type="search" placeholder="🔍 Buscar flor o significado…" autocomplete="off">
  <div class="chips">
@@CHIPS@@
  </div>
@@SECTIONS@@
</main>
<script>
var q = document.getElementById('q');
var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
function norm(s) {
  return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
}
q.addEventListener('input', function () {
  var v = norm(q.value);
  cards.forEach(function (c) {
    c.classList.toggle('hide', norm(c.textContent).indexOf(v) === -1);
  });
  document.querySelectorAll('.month').forEach(function (m) {
    var vis = Array.prototype.some.call(m.querySelectorAll('.card'), function (c) {
      return !c.classList.contains('hide');
    });
    m.style.display = vis ? '' : 'none';
  });
});
document.querySelectorAll('.chip').forEach(function (ch) {
  ch.addEventListener('click', function () {
    var t = document.getElementById(ch.dataset.target);
    if (t) t.scrollIntoView({ behavior: 'smooth' });
  });
});

/* ---------- Candados en días futuros + progreso ---------- */
(function () {
  var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var unlocked = 0;
  cards.forEach(function (c) {
    var p = c.getAttribute('href').replace('dia-', '').replace('.html', '').split('-');
    var mm = parseInt(p[0], 10), dd = parseInt(p[1], 10);
    var year = (mm > 9 || (mm === 9 && dd >= 29)) ? 2026 : 2027;
    if (today >= new Date(year, mm - 1, dd)) { unlocked++; }
    else { c.classList.add('locked'); }
  });
  var msg = '🌸 <strong>' + unlocked + '</strong> de 365 flores desbloqueadas';
  if (unlocked === 0) msg += ' · la primera llega el <strong>29/09/2026</strong>';
  else if (unlocked === 365) msg += ' · ¡calendario completo! 🎉';
  else if (today < new Date(2027, 8, 28)) msg += ' · mañana otra más 🌱';
  document.getElementById('prog').innerHTML = msg;
  document.getElementById('bar').style.width = (unlocked / 365 * 100) + '%';
})();
</script>
</body>
</html>
"""

def build_index(entries):
    groups = []
    for e in entries:
        gid = "g%d%s" % (e["year"], e["mm"])
        if not groups or groups[-1][0] != gid:
            groups.append([gid, "%s %d" % (MESES[int(e["mm"]) - 1].capitalize(), e["year"]), []])
        groups[-1][2].append(e)
    chips = "\n".join('    <button class="chip" data-target="%s">%s</button>' % (gid, label)
                      for gid, label, _ in groups)
    secs = []
    for gid, label, items in groups:
        cards = "\n".join(
            '    <a class="card" href="dia-%s.html"><span class="cdate">%s</span>'
            '<span class="cname">%s</span><span class="cmean">%s</span></a>'
            % (e["key"], e["fshort"], e["name"], e["meaning"]) for e in items)
        secs.append('  <section id="%s" class="month">\n    <h2>%s</h2>\n'
                    '    <div class="grid">\n%s\n    </div>\n  </section>' % (gid, label, cards))
    return DIAS.replace("@@CHIPS@@", chips).replace("@@SECTIONS@@", "\n".join(secs))

def main():
    entries = load()
    (BASE / "flores.js").write_text(build_js(entries), encoding="utf-8")
    for old in BASE.glob("dia-*.html"):
        old.unlink()
    (BASE / "dias.html").write_text(build_index(entries), encoding="utf-8")
    for e in entries:
        (BASE / ("dia-%s.html" % e["key"])).write_text(DAY.replace("@@KEY@@", e["key"]), encoding="utf-8")
    print("OK: flores.js + dias.html + %d paginas dia-MM-DD.html" % len(entries))

if __name__ == "__main__":
    main()
