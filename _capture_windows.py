"""
Captura de audio del sistema en Windows (WASAPI loopback).
Requiere: pip install PyAudioWPatch
"""
import pyaudiowpatch as pyaudio
import struct


class WindowsLoopbackRecorder:
    def list_input_devices(self):
        out = []
        try:
            with pyaudio.PyAudio() as p:
                wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
                default_idx = wasapi_info["defaultOutputDevice"]
                default_speakers = p.get_device_info_by_index(default_idx)
                if default_speakers.get("isLoopbackDevice"):
                    out.append({
                        "index": default_speakers["index"],
                        "name": default_speakers["name"],
                        "default": True,
                    })
                for loopback in p.get_loopback_device_info_generator():
                    out.append({
                        "index": loopback["index"],
                        "name": loopback["name"],
                        "default": False,
                    })
        except Exception as e:
            out.append({"error": str(e)})
        return out

    def record_loop(self, sample_rate, channels, frames_callback, is_stopping):
        chunk = 1024
        try:
            with pyaudio.PyAudio() as p:
                wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
                default_speakers = p.get_device_info_by_index(
                    wasapi_info["defaultOutputDevice"]
                )
                if not default_speakers.get("isLoopbackDevice"):
                    for loopback in p.get_loopback_device_info_generator():
                        if default_speakers["name"] in loopback["name"]:
                            default_speakers = loopback
                            break
                    else:
                        raise RuntimeError(
                            "No se encontró dispositivo loopback. "
                            "Ejecutá: python -m pyaudiowpatch"
                        )
                dev_rate = int(default_speakers["defaultSampleRate"])
                dev_channels = default_speakers["maxInputChannels"]

                def callback(in_data, frame_count, time_info, status):
                    # Pasamos rate y channels para que se guarde el WAV correcto
                    frames_callback(in_data, dev_rate, dev_channels)
                    return (in_data, pyaudio.paContinue)

                with p.open(
                    format=pyaudio.paInt16,
                    channels=dev_channels,
                    rate=dev_rate,
                    frames_per_buffer=chunk,
                    input=True,
                    input_device_index=default_speakers["index"],
                    stream_callback=callback,
                ) as stream:
                    while not is_stopping():
                        import time
                        time.sleep(0.2)
        except Exception as e:
            frames_callback(b"")  # señal de error opcional
            raise RuntimeError(f"Error grabando en Windows: {e}") from e
