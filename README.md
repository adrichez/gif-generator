<p align="center">
  <img src="assets/cover.png" alt="GIF Generator Banner" style="width:100%">
</p>

<div align="center">
  <h1><span style="color: #80c5e5ff;">Genera GIFs a partir de videos y comprímelos automáticamente usando Python</span></h1>

  <hr style="border:none; height:0.3px; background-color:#777; width:65%; margin:30px auto 35px auto;">

  <p>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></a>
    <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white" alt="Git"></a>
    <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" alt="GitHub"></a>
    <a href="https://www.markdownguide.org/"><img src="https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white" alt="Markdown"></a>
  </p>

  <p>
    <a href="## 📄 Descripción">Descripción</a> •
    <a href="## 📂 Estructura del Repositorio">Estructura</a> • 
    <a href="## ⚙️ Requisitos">Requisitos</a> • 
    <a href="## 💻 Instalación">Instalación</a> • 
    <a href="## 🚀 Uso">Uso</a> • 
    <a href="## 📝 Notas">Notas</a> • 
    <a href="## 📌 Opcional">Opcional</a>
    <a href="## 🔧 Licencia">Licencia</a>
  </p>
</div>








<br>

---

## 📄 Descripción

Un script en Python para generar **GIFs a partir de archivos de video** (ej. `.mov`, `.mp4`) y **comprimir GIFs existentes** automáticamente.  
El script permite configurar:

* FPS del GIF  
* Ancho del GIF manteniendo proporción  
* Factor de velocidad del video  
* Número máximo de colores al comprimir (dithering fijo: `bayer`)  

La herramienta es **interactiva**, ejecutable desde la terminal, y guarda los resultados automáticamente en las carpetas `gifs/generated/` y `gifs/compressed/`.  
Además, mientras se genera o comprime el GIF, muestra un **spinner de progreso** y el tiempo de procesamiento, manteniendo la salida limpia.






<br>

---

## 📂 Estructura del Repositorio

```plaintext
gif-generator/
├── assets               # Imagen de portada y otros recursos
├── gifs
│   ├── compressed       # GIFs comprimidos
│   └── generated        # GIFs generados a partir de video
├── gif_generator.py     # Script principal en Python
├── README.md            # Documentación del proyecto
└── requirements.txt     # Dependencias de Python
```






<br>

---

## ⚙️ Requisitos

* Python 3.8 o superior
* [FFmpeg](https://ffmpeg.org/) instalado y accesible en el PATH

Todos los demás módulos (`os`, `sys`, `shutil`, `subprocess`, `pathlib`, `threading`, `itertools`, `time`) están incluidos en la **biblioteca estándar de Python**.






<br>

---

## 💻 Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/tu-usuario/gif-generator.git
cd gif-generator
```

2. **Crear un entorno virtual (recomendado):**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. **Instalar dependencias (si hubiera):**

```bash
pip install -r requirements.txt
```

> ⚠️ Por ahora, `requirements.txt` solo especifica la versión de Python, ya que todas las librerías usadas son estándar.






<br>

---

## 🚀 Uso

Ejecuta el script:

```bash
python gif_generator.py
```

Se mostrará un menú interactivo:

```
Selecciona una opción:
 1) Generar GIF a partir de un video
 2) Comprimir un GIF existente
 3) Salir
```

### 1) Generar GIF a partir de un video

* Ingresa la **ruta del archivo de video**.
* Opcionalmente ajusta:

  * FPS (frames por segundo)
  * Ancho en píxeles (manteniendo proporción)
  * Factor de velocidad (1.0 = normal)

El GIF se guardará automáticamente en `gifs/generated/` con la paleta de colores optimizada generada junto al archivo.

### 2) Comprimir un GIF existente

* Ingresa la **ruta del GIF a comprimir**.
* Opcionalmente ajusta:

  * FPS objetivo
  * Ancho en píxeles
  * Número máximo de colores (1-256)

El GIF comprimido se guarda automáticamente en `gifs/compressed/` con **dithering fijo `bayer`** y su paleta optimizada.

> Durante ambos procesos, un **spinner animado** indicará el progreso y, al finalizar, se muestra el **tiempo empleado** y la **ruta del archivo generado**.






<br>

---

## 📝 Notas

* Los GIFs generados mantienen la **proporción original del video**.
* La paleta de colores se genera automáticamente junto al GIF para optimizar calidad y tamaño.
* La compresión utiliza un **dithering bayer** por defecto, sin preguntar al usuario.
* No se requiere ingresar rutas de salida, se usan carpetas fijas `gifs/generated/` y `gifs/compressed/`.
* Compatible con videos en formatos comunes soportados por FFmpeg (`.mp4`, `.mov`, `.avi`, etc.).






<br>

---

## 📌 Opcional

Para hacer que el script sea ejecutable directamente (macOS/Linux):

```bash
chmod +x gif_generator.py
./gif_generator.py
```






<br>

---

## 🔧 Licencia

Este proyecto es de código abierto bajo la **Licencia MIT**. ¡Libre para usar y modificar!
