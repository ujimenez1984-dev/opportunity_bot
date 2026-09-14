import subprocess
import sys

pasos = [
    ["python3", "scripts/comprobar_catalogo.py"],
    ["python3", "scripts/actualizar_web.py"],
]

for paso in pasos:
    print("Ejecutando:", " ".join(paso))
    resultado = subprocess.run(paso)

    if resultado.returncode != 0:
        print("El proceso se detuvo porque la comprobación no fue correcta.")
        sys.exit(resultado.returncode)

print("Bot terminado correctamente.")
