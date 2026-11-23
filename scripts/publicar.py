"""Genera la web pública (docs/) a partir de app/catequesis.html.

Uso (desde la raíz del repo):
    python3 scripts/publicar.py

Produce:
  docs/index.html          la app completa, instalable en el móvil (PWA)
  docs/catequesis.ics      el calendario al que se suscriben los catequistas
  docs/manifest.webmanifest, docs/sw.js, docs/icon.svg

Los datos del curso están en el bloque <script type="application/json" id="datos">
de app/catequesis.html. Para cambiar fechas, casas o quién prepara: editar ese
bloque, ejecutar este script y subir docs/ (commit + push). GitHub Pages
publica en un minuto; los calendarios suscritos se actualizan en unas horas.
"""
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "app" / "catequesis.html"
DOCS = RAIZ / "docs"

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Europe/Madrid
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""

ICONO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<rect width="512" height="512" rx="112" fill="#1f3a64"/>
<g fill="none" stroke="#f3eee5" stroke-width="30">
<circle cx="208" cy="272" r="92"/><circle cx="304" cy="272" r="92"/>
</g>
<path d="M256 96v84M222 128h68" stroke="#dce7f3" stroke-width="22" stroke-linecap="round"/>
</svg>
"""

CABECERA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Calendario y programa de la catequesis de novios De la mano. Parroquia Reina del Cielo.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="De la mano">
"""

REGISTRO_SW = """<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
</script>
"""

MANIFEST = {
    "name": "Catequesis De la mano para Novios",
    "short_name": "De la mano",
    "lang": "es",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#f3eee5",
    "theme_color": "#1f3a64",
    "icons": [
        {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    ],
}

# Red primero: con conexión siempre se ve lo último; sin conexión, la última copia.
SW = """const CACHE = "de-la-mano-v1";
self.addEventListener("install", e => { self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(r => {
      const copia = r.clone();
      caches.open(CACHE).then(c => c.put(e.request, copia));
      return r;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
"""


def esc_ics(texto: str) -> str:
    return (texto.replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def plegar(linea: str) -> str:
    """Corta líneas a 75 octetos como pide RFC 5545."""
    if len(linea.encode("utf-8")) <= 75:
        return linea
    trozos, actual = [], b""
    for ch in linea:
        b = ch.encode("utf-8")
        if len(actual) + len(b) > (75 if not trozos else 74):
            trozos.append(actual.decode("utf-8"))
            actual = b""
        actual += b
    trozos.append(actual.decode("utf-8"))
    return "\r\n ".join(trozos)


def calendario(d: dict) -> str:
    h, mi = map(int, d["hora"].split(":"))
    sello = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lineas = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Catequesis De la mano para Novios//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Catequesis De la mano",
        "X-WR-CALDESC:" + esc_ics("Catequesis de novios. Parroquia Reina del Cielo. Curso 2026/2027."),
        "X-WR-TIMEZONE:Europe/Madrid",
        "REFRESH-INTERVAL;VALUE=DURATION:PT6H",
        "X-PUBLISHED-TTL:PT6H",
        *VTIMEZONE.splitlines(),
    ]
    for x in d["plan"]:
        s = d["sesiones"][x["s"]]
        casa = d["casas"][x["casa"]]
        ini = datetime.strptime(x["f"], "%Y-%m-%d").replace(hour=h, minute=mi)
        fin = ini + timedelta(minutes=d["duracion_min"])
        temas = ("Temas " + " y ".join(map(str, s["temas"]))) if len(s["temas"]) > 1 else f"Tema {s['temas'][0]}"
        desc = (f"{temas}: {s['titulo']}\n{s['sub']}\n\n"
                f"Prepara: {d['parejas'][x['prepara']]}\n"
                f"Libro: {s['libro']}\n\n{d['web']}")
        lineas += [
            "BEGIN:VEVENT",
            f"UID:catequesis-{x['f']}@catequesis-novios",
            f"DTSTAMP:{sello}",
            f"DTSTART;TZID=Europe/Madrid:{ini:%Y%m%dT%H%M%S}",
            f"DTEND;TZID=Europe/Madrid:{fin:%Y%m%dT%H%M%S}",
            "SUMMARY:" + esc_ics(f"Catequesis de novios: {s['titulo']}"),
            "LOCATION:" + esc_ics(f"{casa['nombre']}, {casa['dir']}, Madrid"),
            "DESCRIPTION:" + esc_ics(desc),
            "URL:" + d["web"],
            "END:VEVENT",
        ]
    lineas.append("END:VCALENDAR")
    return "\r\n".join(plegar(l) for l in lineas) + "\r\n"


def main() -> None:
    app = APP.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/json" id="datos">(.*?)</script>', app, re.S)
    if not m:
        raise SystemExit("No encuentro el bloque de datos en app/catequesis.html")
    d = json.loads(m.group(1))

    corte = app.index('<main class="app">')
    pagina = CABECERA + app[:corte] + "</head>\n<body>\n" + app[corte:] + REGISTRO_SW + "</body>\n</html>\n"

    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(pagina, encoding="utf-8")
    (DOCS / "catequesis.ics").write_bytes(calendario(d).encode("utf-8"))
    (DOCS / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DOCS / "sw.js").write_text(SW, encoding="utf-8")
    (DOCS / "icon.svg").write_text(ICONO, encoding="utf-8")
    print(f"docs/ generado: {len(d['plan'])} sesiones, del {d['plan'][0]['f']} al {d['plan'][-1]['f']}")


if __name__ == "__main__":
    main()
