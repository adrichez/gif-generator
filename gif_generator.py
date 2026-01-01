#!/usr/bin/env python3

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# IMPORTACIÓN DE LIBRERÍAS
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import os
import sys
import shutil
import subprocess
from pathlib import Path
import threading
import itertools
import time








#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# FUNCIONES
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

############################################################################################################
# Funciones auxiliares
############################################################################################################

def clean_path(p: str) -> str:
    if p is None:
        return ""
    return p.strip().strip('\'"')

def ensure_ffmpeg_available():
    if not shutil.which("ffmpeg"):
        print("❌ Error: ffmpeg no está instalado o no está en el PATH.")
        sys.exit(1)

def path_exists_or_exit(p: str, what="archivo"):
    if not os.path.exists(p):
        print(f"❌ No se encontró {what}: {p}")
        sys.exit(1)

def make_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def default_if_empty(value: str, default):
    return default if not value.strip() else value

def int_or_default(val: str, default: int):
    if not val.strip():
        return default
    try:
        return int(val)
    except ValueError:
        print(f"⚠️  Valor no válido, usando por defecto: {default}")
        return default

def float_or_default(val: str, default: float):
    if not val.strip():
        return default
    try:
        return float(val)
    except ValueError:
        print(f"⚠️  Valor no válido, usando por defecto: {default}")
        return default

def build_output_path_from_input(input_path: str, out_dir: str, suffix: str, ext: str = ".gif"):
    p = Path(input_path)
    name = p.stem
    out_name = f"{name}{suffix}{ext}"
    return str(Path(out_dir) / out_name)

def spinner(message="⌛️ Generando GIF..."):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if spinner.stop:
            break
        sys.stdout.write(f'\r{message} {c}')
        sys.stdout.flush()
        time.sleep(0.12)
    sys.stdout.write('\r' + " " * (len(message) + 2) + '\r')






############################################################################################################
# Funciones principales
############################################################################################################

#=================================================================================================
# Función para crear un GIF a partir de un video
#=================================================================================================

def create_gif_from_video(input_file: str, output_file: str,
                        fps: int = 30, width: int = 1280, speed_factor: float = 1.0):
    """
    Genera un GIF a partir de un video usando paleta optimizada.
    - Paleta se guarda junto al GIF.
    - Sin mostrar proceso de FFmpeg, solo spinner con tiempo de ejecución.
    """
    input_file = clean_path(input_file)
    output_file = clean_path(output_file)
    path_exists_or_exit(input_file, what="archivo de video")
    ensure_ffmpeg_available()

    palette_file = str(Path(output_file).with_suffix("")) + "_palette.png"

    print("")
    spinner.stop = False
    t = threading.Thread(target=spinner, args=("⌛️ Generando GIF...",))
    t.start()
    start_time = time.time()

    try:
        # 1) Generar paleta
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", input_file,
            "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
            palette_file
        ], check=True)

        # 2) Generar GIF
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", input_file, "-i", palette_file,
            "-filter_complex",
            f"fps={fps},scale={width}:-1:flags=lanczos,setpts={speed_factor}*PTS[x];[x][1:v]paletteuse",
            output_file
        ], check=True)

    except subprocess.CalledProcessError:
        spinner.stop = True
        t.join()
        print("\n❌ Error: ffmpeg falló al generar el GIF.")
        raise

    # Detener spinner
    spinner.stop = True
    t.join()

    elapsed = time.time() - start_time
    print(f"\n✅ GIF generado correctamente.")
    print(f"⌛️ Tiempo empleado: {elapsed:.1f} segundos.")
    print(f"📁 Archivo disponible en: {output_file}")
    print("🚪 Saliendo del programa...")
    print("👋 ¡Hasta luego!\n")

    return output_file




#=================================================================================================
# Función para comprimir un GIF existente
#=================================================================================================

def compress_gif(input_gif: str,
                fps: int = 15,
                width: int = 900,
                max_colors: int = 200):
    """
    Comprime un GIF reduciendo FPS, resolución y número de colores.
    - Guardado automático en gifs/compressed/
    - Dithering fijo: bayer
    - Paleta se guarda junto al GIF comprimido
    - Sin mostrar proceso de FFmpeg, solo un spinner
    """

    input_gif = clean_path(input_gif)
    path_exists_or_exit(input_gif, what="archivo GIF de entrada")

    output_dir = Path("gifs/compressed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_gif = output_dir / (Path(input_gif).stem + "_compressed.gif")
    palette_file = output_dir / (Path(input_gif).stem + "_palette.png")

    max_colors = max(1, min(max_colors, 256))
    ensure_ffmpeg_available()

    print("")
    spinner.stop = False
    t = threading.Thread(target=spinner, args=("⌛️ Comprimiendo GIF...",))
    t.start()
    start_time = time.time()

    try:
        # 1) Generar paleta
        subprocess.run([
            "ffmpeg", "-v", "error", "-y",
            "-i", input_gif,
            "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen=max_colors={max_colors}",
            str(palette_file)
        ], check=True)

        # 2) Aplicar paleta con dither=bayer
        subprocess.run([
            "ffmpeg", "-v", "error", "-y",
            "-i", input_gif,
            "-i", str(palette_file),
            "-filter_complex",
            f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer",
            str(output_gif)
        ], check=True)

    except subprocess.CalledProcessError:
        spinner.stop = True
        t.join()
        print("\n❌ Error: ffmpeg falló al comprimir el GIF.")
        raise

    spinner.stop = True
    t.join()

    elapsed = time.time() - start_time
    print(f"✅ GIF comprimido correctamente.")
    print(f"⌛️ Tiempo empleado: {elapsed:.1f} segundos.")
    print(f"📁 Archivo disponible en: {output_gif}")
    print("🚪 Saliendo del programa...")
    print("👋 ¡Hasta luego!\n")
    return str(output_gif)






############################################################################################################
# Funciones para interacción con el usuario
############################################################################################################

#=================================================================================================
# Función para modo interactivo de creación de GIFs
#=================================================================================================

def interactive_create_mode(base_generated_dir: str):
    print("\n\n======================================================")
    print("OPCIÓN 1: CREAR UN GIF A PARTIR DE UN VIDEO")
    print("======================================================\n")
    print("Proporcione los siguientes parametros para crear su GIF:")
    print("--------------------------------------------------------")
    input_file = clean_path(input(" -> Ruta del archivo de video (ej: /ruta/mi_video.mov): ").strip())
    if not input_file or not os.path.exists(input_file):
        print("❌ Archivo no válido. Saliendo.")
        return

    fps = int_or_default(input(f" -> FPS [30]: "), 30)
    width = int_or_default(input(f" -> Ancho [1280]: "), 1280)
    speed = float_or_default(input(f" -> Factor de duración [1.0]: "), 1.0)

    out_path = build_output_path_from_input(input_file, base_generated_dir, "_generated")
    os.makedirs(base_generated_dir, exist_ok=True)
    create_gif_from_video(input_file, out_path, fps=fps, width=width, speed_factor=speed)




#=================================================================================================
# Función para modo interactivo de compresión de GIFs
#=================================================================================================

def interactive_compress_mode(base_compressed_dir: str):
    print("\n\n======================================================")
    print("OPCIÓN 2: COMPRIMIR UN GIF EXISTENTE")
    print("======================================================\n")
    print("Proporcione los siguientes parametros para comprimir su GIF:")
    print("------------------------------------------------------------")

    input_gif = clean_path(input(" -> Ruta del GIF a comprimir: ").strip())
    if not input_gif or not os.path.exists(input_gif):
        print("\n❌ Archivo no válido. Saliendo.")
        return

    fps = int_or_default(input(f" -> FPS objetivo [15]: "), 15)
    width = int_or_default(input(f" -> Ancho [900]: "), 900)
    max_colors = int_or_default(input(f" -> Max colors [200]: "), 200)
    max_colors = max(1, min(max_colors, 256))

    os.makedirs(base_compressed_dir, exist_ok=True)
    compress_gif(input_gif, fps=fps, width=width, max_colors=max_colors)






############################################################################################################
# Función principal
############################################################################################################

def main():
    script_dir = os.getcwd()
    base_generated_dir = os.path.join(script_dir, "gifs", "generated")
    base_compressed_dir = os.path.join(script_dir, "gifs", "compressed")
    make_dirs(base_generated_dir, base_compressed_dir)

    print("\n#############################################################################################")
    print("GENERADOR Y COMPRESOR DE GIFS")
    print("#############################################################################################\n")
    print("¿Qué desea hacer en el programa?")
    print("--------------------------------")
    print(" 1) Generar un GIF a partir de un video")
    print(" 2) Comprimir un GIF existente")
    print(" 3) Salir del programa")
    choice = input(" -> Selecciona (1/2/3): ")

    ensure_ffmpeg_available()
    if choice == "1":
        interactive_create_mode(base_generated_dir)
    elif choice == "2":
        interactive_compress_mode(base_compressed_dir)
    elif choice == "3":
        print("\n🚪Saliendo del programa.")
        print("👋¡Hasta luego!\n")
    else:
        print("\n❌ Opción no válida.")
        print("🙏 Por favor, ejecuta el script de nuevo y selecciona una opción válida.\n")








#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# EJECUCIÓN PRINCIPAL DEL SCRIPT
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

if __name__ == "__main__":
    main()
