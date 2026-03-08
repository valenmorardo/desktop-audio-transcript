"""
Captura de audio del sistema en Windows (WASAPI loopback, PyAudioWPatch).
"""
import sys
import threading
import tempfile
import wave
from pathlib import Path

SAMPLE_RATE = 16000  # Whisper trabaja bien con 16 kHz
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16 bit


def _get_platform_recorder():
    if sys.platform != "win32":
        raise RuntimeError("Esta app está configurada solo para Windows.")
    from _capture_windows import WindowsLoopbackRecorder
    return WindowsLoopbackRecorder()


class SystemAudioRecorder:
    """
    Graba el audio que sale del sistema (Zoom, Meet, etc.).
    Uso: start() -> ... -> stop() -> get_wav_path() o get_wav_bytes().
    """

    def __init__(self):
        self._impl = _get_platform_recorder()
        self._frames = []
        self._sample_rate = SAMPLE_RATE
        self._channels = CHANNELS
        self._recording = False
        self._thread = None
        self._record_error = None  # excepción del hilo de grabación

    def start(self):
        """Empieza a grabar."""
        if self._recording:
            return
        self._frames = []
        self._sample_rate = SAMPLE_RATE
        self._channels = CHANNELS
        self._record_error = None
        self._recording = True
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Deja de grabar."""
        self._recording = False
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None

    def _on_frames(self, data, sample_rate=None, channels=None):
        self._frames.append(data)
        if sample_rate is not None:
            self._sample_rate = sample_rate
        if channels is not None:
            self._channels = channels

    def _record_loop(self):
        try:
            self._impl.record_loop(
                sample_rate=SAMPLE_RATE,
                channels=CHANNELS,
                frames_callback=self._on_frames,
                is_stopping=lambda: not self._recording,
            )
        except Exception as e:
            self._record_error = e

    def get_last_error(self):
        """Devuelve el mensaje de error de la última grabación, o None."""
        if self._record_error is None:
            return None
        return str(self._record_error)

    def get_wav_path(self) -> Path | None:
        """Guarda la grabación en un WAV temporal y devuelve la ruta. None si no hay datos."""
        if not self._frames:
            return None
        data = b"".join(self._frames)
        path = Path(tempfile.gettempdir()) / f"desktop_transcript_{id(self)}.wav"
        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(self._channels)
            wav.setsampwidth(SAMPLE_WIDTH)
            wav.setframerate(self._sample_rate)
            wav.writeframes(data)
        return path

    def get_wav_bytes(self) -> bytes | None:
        """Devuelve el WAV en memoria. None si no hay datos."""
        if not self._frames:
            return None
        import io
        data = b"".join(self._frames)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav:
            wav.setnchannels(self._channels)
            wav.setsampwidth(SAMPLE_WIDTH)
            wav.setframerate(self._sample_rate)
            wav.writeframes(data)
        return buf.getvalue()

    def list_input_devices(self):
        """Lista dispositivos de captura disponibles (para elegir monitor en Linux)."""
        return self._impl.list_input_devices()
