"""
Captura de audio del sistema en Linux (monitor de PulseAudio/PipeWire).
Requiere: sounddevice (y PulseAudio o PipeWire).
"""
import sounddevice as sd
import numpy as np


def _find_monitor_device():
    """Devuelve el índice del dispositivo 'Monitor' (salida del sistema) o None."""
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] == 0:
            continue
        name = (dev.get("name") or "").lower()
        if "monitor" in name:
            return i
    return None


class LinuxMonitorRecorder:
    def list_input_devices(self):
        out = []
        try:
            devices = sd.query_devices()
            default = sd.default.device[0]
            for i, dev in enumerate(devices):
                if dev["max_input_channels"] == 0:
                    continue
                out.append({
                    "index": i,
                    "name": dev.get("name", "?"),
                    "default": i == default,
                    "is_monitor": "monitor" in (dev.get("name") or "").lower(),
                })
        except Exception as e:
            out.append({"error": str(e)})
        return out

    def record_loop(self, sample_rate, channels, frames_callback, is_stopping):
        device = _find_monitor_device()
        if device is None:
            raise RuntimeError(
                "No se encontró ningún dispositivo 'Monitor' (audio de salida). "
                "En Linux, el audio de Zoom/Meet se captura desde el monitor de PulseAudio/PipeWire. "
                "Listá dispositivos con: python -c \"import sounddevice; print(sounddevice.query_devices())\""
            )
        chunk_frames = 1024
        block_duration = chunk_frames / sample_rate

        def callback(indata, frame_count, time_info, status):
            if status:
                pass  # opcional: log
            # indata es (frames, channels), 16-bit sería dtype int16
            data = (indata * 32767).astype(np.int16).tobytes()
            frames_callback(data, sample_rate, channels)

        try:
            with sd.InputStream(
                device=device,
                channels=channels,
                samplerate=sample_rate,
                dtype="float32",
                blocksize=chunk_frames,
                callback=callback,
            ):
                while not is_stopping():
                    sd.sleep(int(block_duration * 1000))
        except Exception as e:
            raise RuntimeError(f"Error grabando en Linux: {e}") from e
