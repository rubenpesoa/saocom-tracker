import requests
import os

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "TLE.txt")

def descargar_tle():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()
    return response.text

def filtrar_saocom(tle_text):
    lineas = tle_text.splitlines()
    resultado = []

    for i in range(0, len(lineas), 3):
        if i + 2 >= len(lineas):
            continue

        nombre = lineas[i].strip()

        if "SAOCOM 1A" in nombre or "SAOCOM 1B" in nombre:
            resultado.append(nombre)
            resultado.append(lineas[i + 1].strip())
            resultado.append(lineas[i + 2].strip())

    return "\n".join(resultado)

def guardar_archivo(contenido):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(contenido)

def main():
    print("Descargando TLE...")
    tle_data = descargar_tle()

    print("Filtrando SAOCOM 1A y 1B...")
    tle_filtrado = filtrar_saocom(tle_data)

    if not tle_filtrado.strip():
        print("No se encontraron TLE de SAOCOM 1A o 1B.")
        return

    print("Guardando archivo...")
    guardar_archivo(tle_filtrado)

    print(f"Listo. Archivo actualizado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()