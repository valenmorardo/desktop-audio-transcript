# Guía paso a paso — Windows

Esta guía es para usar la app **solo en Windows**. Flujo: clonar → ejecutar un script → listo.

---

## Requisitos previos

- **Python 3.10 o 3.11** instalado y en el PATH.  
  Descarga: [python.org/downloads](https://www.python.org/downloads/). Al instalar, marcá **"Add Python to PATH"**.
- **ffmpeg** en el PATH (lo usa faster-whisper).  
  Descarga: [ffmpeg.org/download.html](https://ffmpeg.org/download.html), o con Chocolatey: `choco install ffmpeg`.

### Cómo verificar

En **cmd** o **PowerShell**:

| Qué     | Comando              | Si está bien                    |
|--------|----------------------|----------------------------------|
| Python | `python --version`   | Ej. `Python 3.10.x` o `3.11.x`   |
| ffmpeg | `ffmpeg -version`    | Muestra la versión              |

Si no está, el script `iniciar.bat` te avisará al intentar abrir la app.

---

## Uso en 3 pasos

### 1. Clonar el repositorio

En **cmd** o **PowerShell**:

```cmd
git clone https://github.com/valenmorardo/desktop-audio-transcript.git
cd desktop-audio-transcript
```

(O descargá el ZIP del repo y descomprimilo; después entrá a la carpeta.)

### 2. Ejecutar el script

Doble clic en **`iniciar.bat`**  
**o** desde cmd en esa carpeta:

```cmd
iniciar.bat
```

El script:

- Crea el entorno virtual (`venv`) si no existe.
- Instala o actualiza las dependencias (`pip install -r requirements.txt`).
- Abre la app.

La primera vez puede tardar un poco (descarga de paquetes y, al transcribir, el modelo de IA). Las siguientes veces solo abre la app.

### 3. Usar la app

1. Clic en **Empezar a escuchar** (empieza a grabar el audio del sistema).
2. Reproducí la clase (Zoom, Meet, etc.) o cualquier audio.
3. Clic en **Dejar de escuchar**.
4. Clic en **Transcribir** (la primera vez descargará el modelo "base").
5. Revisá el texto y usá **Guardar transcript en archivo** si querés.

---

## Resumen

| Paso   | Acción |
|--------|--------|
| 1      | Clonar (o descargar) el repo y entrar a la carpeta. |
| 2      | Ejecutar `iniciar.bat`. |
| 3      | Usar la app: Empezar a escuchar → Dejar de escuchar → Transcribir. |

No hace falta activar el venv a mano ni revisar dependencias una por una: el script se encarga.

---

## Si algo falla

- **"No se encontró Python"** → Instalá Python desde python.org y marcá "Add Python to PATH". Cerrá y volvé a abrir cmd.
- **"ffmpeg no está en el PATH"** → Instalá ffmpeg y agregalo al PATH, o instalalo con Chocolatey: `choco install ffmpeg`.
- **No se captura audio** → Ejecutá `python -m pyaudiowpatch` (con el venv activado: `venv\Scripts\activate`) para ver los dispositivos de audio; en la app se usa el dispositivo de salida por defecto como loopback.
