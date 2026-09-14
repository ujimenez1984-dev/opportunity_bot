import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

archivo = Path("data/oportunidades.json")
oportunidades = json.loads(archivo.read_text(encoding="utf-8"))

if not isinstance(oportunidades, list) or not oportunidades:
    raise SystemExit("Error: el catálogo está vacío.")

obligatorios = {"titulo", "categoria", "descripcion", "enlace"}
enlaces_vistos = set()

for numero, producto in enumerate(oportunidades, start=1):
    faltan = obligatorios - producto.keys()

    if faltan:
        raise SystemExit(
            f"Error en el producto {numero}: faltan {', '.join(sorted(faltan))}"
        )

    for campo in ("titulo", "categoria", "descripcion", "enlace"):
        if not str(producto[campo]).strip():
            raise SystemExit(
                f"Error en el producto {numero}: el campo «{campo}» está vacío."
            )

    enlace = producto["enlace"].strip()
    partes = urlparse(enlace)
    parametros = parse_qs(partes.query)

    if partes.scheme != "https" or partes.netloc != "www.amazon.es":
        raise SystemExit(
            f"Error en el producto {numero}: el enlace no es de Amazon España."
        )

    if parametros.get("tag") != ["radaroportu01-21"]:
        raise SystemExit(
            f"Error en el producto {numero}: falta el ID de afiliado correcto."
        )

    if enlace in enlaces_vistos:
        raise SystemExit(
            f"Error: el enlace del producto {numero} está duplicado."
        )

    enlaces_vistos.add(enlace)

print(f"Catálogo correcto: {len(oportunidades)} productos con enlaces de afiliado válidos.")
