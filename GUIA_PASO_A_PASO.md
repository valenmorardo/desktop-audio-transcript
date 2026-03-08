# Guía paso a paso — Instalación y prueba

Esta guía explica cómo clonar el repositorio, instalar dependencias y probar la app en **Linux** y en **Windows**.

---

## Requisitos previos (ambos sistemas)

- **Python 3.10 o 3.11** instalado y en el PATH.
- **ffmpeg** instalado y en el PATH (lo usa faster-whisper).
- **Git** (para clonar el repo).

---

# Linux

## 1. Clonar el repositorio

Abrí una terminal y elegí la carpeta donde querés el proyecto. Luego:

```bash
git clone https://github.com/valenmorardo/desktop-audio-transcript.git
cd desktop-audio-transcript
```

*(Reemplazá `valenmorardo` por tu usuario de GitHub; si el repo tiene otro nombre o URL, usá esa.)*

## 2. Crear el entorno virtual

```bash
python3 -m venv venv
```

## 3. Activar el entorno virtual

```bash
source venv/bin/activate
```

Verás algo como `(venv)` al inicio de la línea. A partir de acá los comandos `pip` y `python` usan ese entorno.

## 4. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

En Linux se instalan, entre otras: `faster-whisper`, `sounddevice`, `soundfile`, `numpy`. **No** se instala PyAudioWPatch (solo se usa en Windows).

## 5. (Opcional) Verificar ffmpeg

```bash
ffmpeg -version
```

Si no está instalado, en Ubuntu/Debian: `sudo apt install ffmpeg`. En Fedora: `sudo dnf install ffmpeg`.

## 6. Ejecutar la aplicación

```bash
python app.py
```

Debería abrirse la ventana de la app.

## 7. Probar el flujo

1. Clic en **Empezar a escuchar** (empieza a grabar el audio del sistema).
2. Reproducí algo (YouTube, Zoom, música) unos segundos.
3. Clic en **Dejar de escuchar**.
4. Clic en **Transcribir** (la primera vez descargará el modelo "base", ~150 MB).
5. Revisá el texto en el cuadro y, si querés, usá **Guardar transcript en archivo**.

## 8. Si no se captura audio (Linux)

Listá los dispositivos de audio:

```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

Tiene que aparecer algún dispositivo con **"Monitor"** en el nombre (salida del sistema). Si no hay, revisá la sección "Si no se captura audio" del [README](README.md).

---

# Windows

## 1. Clonar el repositorio

Abrí **PowerShell** o **Símbolo del sistema** (cmd) y andá a la carpeta donde querés el proyecto:

```cmd
git clone https://github.com/valenmorardo/desktop-audio-transcript.git
cd desktop-audio-transcript
```

*(Reemplazá `valenmorardo` por tu usuario de GitHub.)*

## 2. Crear el entorno virtual

```cmd
python -m venv venv
```

Si `python` no se reconoce, probá `py -m venv venv` o agregá Python al PATH.

## 3. Activar el entorno virtual

En **PowerShell**:

```powershell
.\venv\Scripts\Activate.ps1
```

En **cmd**:

```cmd
venv\Scripts\activate.bat
```

Verás `(venv)` al inicio de la línea.

## 4. Instalar dependencias

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

En Windows, además del resto, se instala **PyAudioWPatch** (captura del audio del sistema vía WASAPI loopback).

## 5. (Opcional) Verificar ffmpeg

```cmd
ffmpeg -version
```

Si no está instalado, descargalo desde [ffmpeg.org](https://ffmpeg.org/download.html) y agregalo al PATH, o usá un gestor como Chocolatey: `choco install ffmpeg`.

## 6. Ejecutar la aplicación

```cmd
python app.py
```

Debería abrirse la ventana de la app.

## 7. Probar el flujo

1. Clic en **Empezar a escuchar**.
2. Reproducí algo (Zoom, Meet, YouTube, etc.) unos segundos.
3. Clic en **Dejar de escuchar**.
4. Clic en **Transcribir** (la primera vez se descargará el modelo "base").
5. Revisá el transcript y usá **Guardar transcript en archivo** si querés.

## 8. Si no se captura audio (Windows)

Para ver los dispositivos WASAPI/loopback:

```cmd
python -m pyaudiowpatch
```

Revisá la sección "Si no se captura audio" del [README](README.md) si algo falla.

---

# Resumen rápido (después de clonar)

| Paso | Linux | Windows |
|------|--------|---------|
| Entorno virtual | `python3 -m venv venv` | `python -m venv venv` |
| Activar | `source venv/bin/activate` | `.\venv\Scripts\Activate.ps1` o `venv\Scripts\activate.bat` |
| Dependencias | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Ejecutar | `python app.py` | `python app.py` |

---

# Volver a probar más adelante (repo ya clonado)

```bash
# Linux
cd desktop-audio-transcript
source venv/bin/activate
git pull
pip install -r requirements.txt
python app.py
```

```cmd
# Windows
cd desktop-audio-transcript
venv\Scripts\activate
git pull
pip install -r requirements.txt
python app.py
```

Si agregás o cambiás dependencias en el repo, `pip install -r requirements.txt` actualiza el entorno.
