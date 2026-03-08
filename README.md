# Transcripción de clases (audio de escritorio)

App de escritorio para **Windows** que graba el audio que suena en la PC (Zoom, Google Meet, etc.) y lo **transcribe a texto** con IA en local (faster-whisper). Pensado para tener el transcript de clases virtuales para estudiar.

**Flujo:** abrís la app → **Empezar a escuchar** → escuchás la clase → **Dejar de escuchar** → **Transcribir** → guardás el texto.

---

## Uso rápido (recomendado)

1. **Clonar** el repo (o descargar y descomprimir).
2. En la carpeta del proyecto, **doble clic en `iniciar.bat`** (o desde cmd: `iniciar.bat`).
3. La primera vez crea el entorno, instala dependencias y abre la app. Las siguientes veces solo abre la app.

Solo hace falta tener **Python** y **ffmpeg** instalados (ver abajo). El script te avisa si falta algo.

---

## Requisitos (Windows)

- **Python 3.10 o 3.11** — [python.org/downloads](https://www.python.org/downloads/). Al instalar, marcá **"Add Python to PATH"**.
- **ffmpeg** — [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (o `choco install ffmpeg`) y que esté en el PATH.

---

## Cómo usar la app

1. **Empezar a escuchar**: empieza a grabar todo lo que suena en la PC.
2. **Dejar de escuchar**: detiene la grabación.
3. **Transcribir**: convierte la grabación a texto (la primera vez descarga el modelo "base", ~150 MB).
4. **Guardar transcript en archivo**: guardás el texto en `.txt` o `.md`.

---

## Si no se captura audio (Windows)

Ejecutá en cmd (con el venv activado):

```cmd
python -m pyaudiowpatch
```

Ahí ves los dispositivos WASAPI/loopback. Si el que usás para escuchar no aparece como loopback, probá con otro dispositivo de salida por defecto en Windows.

---

## Estructura del proyecto

- `iniciar.bat` — script para instalar y ejecutar la app (usar este).
- `app.py` — ventana con botones y transcripción.
- `audio_capture.py` — grabación de audio del sistema (Windows).
- `_capture_windows.py` — captura WASAPI loopback.
- `transcription.py` — transcripción con faster-whisper.
- `requirements.txt` — dependencias.
