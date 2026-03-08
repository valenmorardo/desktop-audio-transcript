"""
Transcripción de audio con faster-whisper (local).
"""
from pathlib import Path


def transcribe_file(
    audio_path: str | Path,
    model_size: str = "base",
    language: str | None = None,
    device: str = "auto",
) -> str:
    """
    Transcribe un archivo de audio a texto.
    model_size: "tiny", "base", "small", "medium", "large-v3", etc.
    language: código ISO (ej. "es") o None para detección automática.
    """
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device=device, compute_type="default")
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
        vad_filter=True,
    )
    if info.language_probability and info.language:
        # opcional: usar info.language si querés forzar
        pass
    lines = []
    for s in segments:
        lines.append(s.text.strip())
    return "\n".join(filter(None, lines)).strip()
