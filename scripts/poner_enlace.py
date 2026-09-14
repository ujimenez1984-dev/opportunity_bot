import json
from pathlib import Path

enlace = input("Pega aquí el enlace completo de Amazon y pulsa Enter: ").strip()

if not enlace.startswith("https://"):
    raise SystemExit("El enlace no parece válido: debe empezar por https://")

archivo = Path("data/oportunidades.json")
oportunidades = json.loads(archivo.read_text(encoding="utf-8"))

oportunidades[0] = {
    "titulo": "INIU Power Bank 10.000 mAh y 45 W",
    "categoria": "Recomendación destacada",
    "descripcion": "Batería externa compacta con carga rápida. Una opción interesante para viajes, trabajo y uso diario.",
    "enlace": enlace
}

archivo.write_text(
    json.dumps(oportunidades, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)

print("Producto añadido correctamente.")
