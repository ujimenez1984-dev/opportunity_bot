from pathlib import Path

archivo = Path("web/index.html")
etiqueta = input("Pega aquí la etiqueta HTML de Google y pulsa Enter: ").strip()

if "<meta" not in etiqueta or "google-site-verification" not in etiqueta:
    raise SystemExit("La etiqueta no parece ser la de verificación de Google.")

texto = archivo.read_text(encoding="utf-8")

if "google-site-verification" in texto:
    print("Ya existe una etiqueta de verificación en la web.")
else:
    texto = texto.replace("</head>", f"  {etiqueta}\n</head>", 1)
    archivo.write_text(texto, encoding="utf-8")
    print("Etiqueta de Google añadida correctamente.")
