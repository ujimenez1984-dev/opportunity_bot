import html
import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent
archivo_datos = base / "data" / "guias.json"
archivo_web = base / "web" / "index.html"

guias = json.loads(archivo_datos.read_text(encoding="utf-8"))

secciones = []

for guia in guias:
    titulo = html.escape(guia["titulo"])
    categoria = html.escape(guia["categoria"])
    introduccion = html.escape(guia["introduccion"])
    conclusion = html.escape(guia["conclusion"])

    puntos = "\n".join(
        f"<li>{html.escape(punto)}</li>"
        for punto in guia["puntos"]
    )

    secciones.append(
        f"""<article class="bloque">
  <p><strong>{categoria}</strong></p>
  <h2>{titulo}</h2>
  <p>{introduccion}</p>
  <ul class="lista">
    {puntos}
  </ul>
  <p>{conclusion}</p>
</article>"""
    )

inicio = "<!-- GUIDES_START -->"
fin = "<!-- GUIDES_END -->"

seccion_completa = (
    f"{inicio}\n"
    + "\n".join(secciones)
    + f"\n{fin}"
)

texto = archivo_web.read_text(encoding="utf-8")

if inicio in texto and fin in texto:
    antes = texto.split(inicio, 1)[0]
    despues = texto.split(fin, 1)[1]
    texto = antes + seccion_completa + despues
else:
    texto = texto.replace(
        "  </main>",
        f"    {seccion_completa.replace(chr(10), chr(10) + '    ')}\n  </main>",
        1
    )

archivo_web.write_text(texto, encoding="utf-8")

print(f"Guías añadidas: {len(guias)}")
