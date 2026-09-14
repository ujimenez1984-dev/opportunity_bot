import html
import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent
datos = base / "data" / "oportunidades.json"
pagina = base / "web" / "index.html"

with datos.open("r", encoding="utf-8") as archivo:
    oportunidades = json.load(archivo)

elementos = []

for oportunidad in oportunidades:
    titulo = html.escape(str(oportunidad.get("titulo", "")).strip())
    categoria = html.escape(str(oportunidad.get("categoria", "")).strip())
    descripcion = html.escape(str(oportunidad.get("descripcion", "")).strip())
    enlace = str(oportunidad.get("enlace", "")).strip()

    if enlace and not enlace.startswith("https://"):
        raise SystemExit(
            f"Enlace no seguro para «{titulo}». Debe empezar por https://"
        )

    if enlace:
        accion = (
            f'<a href="{html.escape(enlace, quote=True)}" '
            f'rel="nofollow sponsored">Ver recomendación</a>'
        )
    else:
        accion = "<em>Guía editorial; enlace de compra pendiente.</em>"

    elementos.append(
        f"<li><strong>{titulo}</strong><br>"
        f"<small>{categoria}</small><br>"
        f"{descripcion}<br>{accion}</li>"
    )

if elementos:
    contenido = "\n".join(elementos)
else:
    contenido = "<li>Estamos preparando nuevas oportunidades.</li>"

seccion = f"""<!-- BOT_OPPORTUNITIES_START -->
<section class="bloque" id="oportunidades">
  <h2>Oportunidades y guías</h2>
  <p>Contenido seleccionado para ayudarte a comparar antes de comprar.</p>
  <ul class="lista">
    {contenido}
  </ul>
  <p class="nota">Los enlaces de compra se añadirán únicamente cuando la información esté revisada.</p>
</section>
<!-- BOT_OPPORTUNITIES_END -->"""

texto = pagina.read_text(encoding="utf-8")
inicio = "<!-- BOT_OPPORTUNITIES_START -->"
fin = "<!-- BOT_OPPORTUNITIES_END -->"

if inicio in texto and fin in texto:
    antes = texto.split(inicio, 1)[0]
    despues = texto.split(fin, 1)[1]
    texto = antes + seccion + despues
else:
    texto = texto.replace("</main>", seccion + "\n</main>", 1)

pagina.write_text(texto, encoding="utf-8")
print(f"Web actualizada con {len(oportunidades)} oportunidades.")
