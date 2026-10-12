# vscode-espa/icons/crear_icono.py
# genera un icono PNG simple de 128x128 para la extensión Espa+

import struct
import zlib
import os


def crear_png(ruta, ancho=128, alto=128):
    # colores
    azul = (30, 64, 175)
    blanco = (255, 255, 255)

    # construir la matriz de píxeles
    def color_de(x, y):
        # fondo azul
        # franja blanca diagonal simple con "E+" estilizado
        cx = x - ancho // 2
        cy = y - alto // 2

        # E mayúscula
        if -35 <= cx <= -10 and -35 <= cy <= 35:
            # barra horizontal central
            if -5 <= cy <= 5:
                return blanco
            # barra horizontal superior
            if 25 <= cy <= 35:
                return blanco
            # barra horizontal inferior
            if -35 <= cy <= -25:
                return blanco
            # barra vertical izquierda
            if -35 <= cx <= -25:
                return blanco

        # + (más)
        if 5 <= cx <= 15 and -30 <= cy <= 30:
            return blanco
        if -5 <= cy <= 5 and -15 <= cx <= 25:
            return blanco

        return azul

    # construir filas con filtro 0 (sin filtro)
    filas = bytearray()
    for y in range(alto):
        filas.append(0)  # filtro por fila
        for x in range(ancho):
            r, g, b = color_de(x, y)
            filas.append(r)
            filas.append(g)
            filas.append(b)

    # comprimir
    datos = zlib.compress(bytes(filas), 9)

    # chunk helper
    def chunk(tipo, contenido):
        c = struct.pack(">I", len(contenido))
        c += tipo
        c += contenido
        c += struct.pack(">I", zlib.crc32(tipo + contenido) & 0xFFFFFFFF)
        return c

    # IHDR
    ihdr = struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0)

    # construir archivo
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", datos)
    png += chunk(b"IEND", b"")

    with open(ruta, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    ruta = os.path.join(os.path.dirname(__file__), "espa.png")
    crear_png(ruta)
    print(f"icono creado: {ruta}")