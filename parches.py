
from pathlib import Path
from PIL import Image
import numpy as np

# ==========================================
# CONFIGURACIÓN
# ==========================================

RUTA_IMAGES = Path("dataset/images")
RUTA_MASKS = Path("dataset/masks")

RUTA_SALIDA = Path("datasetaumentado")

CARPETA_IMAGES = RUTA_SALIDA / "parcheimage"
CARPETA_MASKS = RUTA_SALIDA / "parchemask"

FILAS = 3
COLUMNAS = 3

EXTENSIONES = {".ppm", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}

# ==========================================
# CREAR CARPETAS
# ==========================================

CARPETA_IMAGES.mkdir(parents=True, exist_ok=True)
CARPETA_MASKS.mkdir(parents=True, exist_ok=True)

# ==========================================
# OBTENER IMÁGENES
# ==========================================

imagenes = sorted([
    p for p in RUTA_IMAGES.iterdir()
    if p.suffix.lower() in EXTENSIONES
])

total_parches = 0

# ==========================================
# PROCESAMIENTO
# ==========================================

for ruta_img in imagenes:

    ruta_mask = RUTA_MASKS / ruta_img.name

    if not ruta_mask.exists():
        print(f"[ERROR] Máscara no encontrada: {ruta_img.name}")
        continue

    img = Image.open(ruta_img)
    mask = Image.open(ruta_mask)

    if img.size != mask.size:
        print(f"[ERROR] Dimensiones diferentes: {ruta_img.name}")
        continue

    ancho, alto = img.size

    print(f"\nProcesando: {ruta_img.name}")
    print(f"Resolución: {ancho} x {alto}")

    # Límites para evitar pérdidas por redondeo
    x_edges = [round(i * ancho / COLUMNAS)
               for i in range(COLUMNAS + 1)]

    y_edges = [round(i * alto / FILAS)
               for i in range(FILAS + 1)]

    contador = 1

    for fila in range(FILAS):

        for columna in range(COLUMNAS):

            izquierda = x_edges[columna]
            derecha = x_edges[columna + 1]

            superior = y_edges[fila]
            inferior = y_edges[fila + 1]

            caja = (
                izquierda,
                superior,
                derecha,
                inferior
            )

            parche_img = img.crop(caja)
            parche_mask = mask.crop(caja)

            nombre = (
                f"{ruta_img.stem}_patch_{contador:02d}.ppm"
            )

            parche_img.save(CARPETA_IMAGES / nombre)
            parche_mask.save(CARPETA_MASKS / nombre)

            contador += 1
            total_parches += 1

    img.close()
    mask.close()

# ==========================================
# RESUMEN
# ==========================================

print("\n================================")
print("PROCESO FINALIZADO")
print("================================")

print(f"Imágenes originales: {len(imagenes)}")
print(f"Total de parches: {total_parches}")

print(f"Imágenes: {CARPETA_IMAGES}")
print(f"Máscaras: {CARPETA_MASKS}")
