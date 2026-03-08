# Transcripción de clases (audio de escritorio)

App de escritorio para **grabar el audio que suena en la PC** (Zoom, Google Meet, etc.) y **transcribirlo a texto** con IA en local (faster-whisper). Pensado para tener el transcript de clases virtuales para estudiar.

**Flujo:** abrís la app → **Empezar a escuchar** → escuchas la clase → **Dejar de escuchar** → **Transcribir** → guardás el texto.

Funciona en **Windows** y **Linux** (desarrollado en Linux, usable en ambos).

---

## Requisitos

- Python 3.10+ (recomendado 3.10 o 3.11)
- **ffmpeg** instalado y en el PATH (faster-whisper lo usa)
- En **Windows**: nada extra (se usa WASAPI loopback).
- En **Linux**: PulseAudio o PipeWire (casi todas las distros lo traen).

---

## Instalación

```bash
cd desktop-audio-transcript
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

En **Windows**, `requirements.txt` instala también **PyAudioWPatch** (captura del audio del sistema). En Linux se usa **sounddevice** con el dispositivo "Monitor".

La primera vez que transcribas, faster-whisper descargará el modelo "base" (unos ~150 MB).

---

## Cómo usar

1. Ejecutá la app:
   ```bash
   python app.py
   ```
2. **Empezar a escuchar**: empieza a grabar todo lo que suena en la PC (Zoom, Meet, música, etc.).
3. **Dejar de escuchar**: detiene la grabación.
4. **Transcribir**: convierte la grabación a texto (puede tardar un poco según la duración).
5. **Guardar transcript en archivo**: guardás el texto en `.txt` o `.md`.

---

## Modelo de IA

Se usa **faster-whisper** (open source, mismo tipo de modelo que Whisper de OpenAI), corriendo **en tu máquina**. No se envía audio a internet. Por defecto el modelo es `base` (buen equilibrio velocidad/calidad). Podés cambiarlo en `transcription.py` (`model_size`: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large-v3"`).

---

## Si no se captura audio

- **Linux:** hace falta un dispositivo de captura que sea el **monitor** de la salida (PulseAudio/PipeWire). Si no aparece, listá dispositivos con:
  ```bash
  python -c "import sounddevice; print(sounddevice.query_devices())"
  ```
  Deberías ver algo como "Monitor of …". Si no hay monitor, en algunos entornos hay que crear un "loopback" o elegir "Monitor of Built-in Audio" (o similar) en la configuración de audio.

- **Windows:** si falla la captura, probá:
  ```bash
  python -m pyaudiowpatch
  ```
  para ver los dispositivos WASAPI y loopback disponibles.

---

## Estructura del proyecto

- `app.py` — ventana con botones Empezar / Dejar de escuchar y Transcribir.
- `audio_capture.py` — grabación de audio del sistema (abstracción multiplataforma).
- `_capture_windows.py` — captura en Windows (WASAPI loopback).
- `_capture_linux.py` — captura en Linux (monitor PulseAudio/PipeWire).
- `transcription.py` — transcripción con faster-whisper.
- `requirements.txt` — dependencias.
