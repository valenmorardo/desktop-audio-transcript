"""
App de escritorio: grabar audio del sistema y transcribir con IA (faster-whisper).
Uso: python app.py
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from pathlib import Path

from audio_capture import SystemAudioRecorder
from transcription import transcribe_file


def main():
    root = tk.Tk()
    root.title("Transcripción de clases — audio de escritorio")
    root.minsize(500, 400)
    root.geometry("700x550")

    recorder = SystemAudioRecorder()
    wav_path_after_stop = None

    # Estado
    status_text = tk.StringVar(value="Listo. Clic en «Empezar a escuchar» para grabar el audio del sistema.")
    transcript_text = tk.StringVar(value="")

    # --- Controles
    f_buttons = ttk.Frame(root, padding=10)
    f_buttons.pack(fill=tk.X)

    btn_start = ttk.Button(
        f_buttons,
        text="Empezar a escuchar",
        command=lambda: _start(recorder, status_text, btn_start, btn_stop),
    )
    btn_start.pack(side=tk.LEFT, padx=(0, 8))

    btn_stop = ttk.Button(
        f_buttons,
        text="Dejar de escuchar",
        state=tk.DISABLED,
    )
    btn_stop.pack(side=tk.LEFT, padx=(0, 8))

    btn_transcribe = ttk.Button(
        f_buttons,
        text="Transcribir",
        state=tk.DISABLED,
        command=lambda: _run_transcribe(wav_path_after_stop, status_text, transcript_area, btn_transcribe, root),
    )
    btn_transcribe.pack(side=tk.LEFT, padx=(0, 8))

    ttk.Label(f_buttons, textvariable=status_text).pack(side=tk.LEFT, padx=(12, 0))

    # --- Área de transcript
    ttk.Label(root, text="Transcript:", font=("", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 0))
    transcript_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, font=("Consolas", 10))
    transcript_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

    btn_save = ttk.Button(
        root,
        text="Guardar transcript en archivo",
        command=lambda: _save_transcript(transcript_area),
    )
    btn_save.pack(pady=6)

    def on_closing():
        if recorder._recording:
            recorder.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    def _stop_cmd():
        nonlocal wav_path_after_stop
        recorder.stop()
        wav_path_after_stop = recorder.get_wav_path()
        err = recorder.get_last_error()
        if wav_path_after_stop:
            status_text.set("Grabación detenida. Clic en «Transcribir» para generar el texto.")
        else:
            msg = "Grabación detenida. No se capturó audio."
            if err:
                msg += " " + err
            else:
                msg += " Comprobá el dispositivo de captura (en Linux hace falta un dispositivo «Monitor»)."
            status_text.set(msg)
            if err:
                messagebox.showwarning("Sin audio", msg + "\n\nVer README o GUIA_PASO_A_PASO.md → «Si no se captura audio».")
        btn_start.config(state=tk.NORMAL)
        btn_stop.config(state=tk.DISABLED)
        if wav_path_after_stop:
            btn_transcribe.config(state=tk.NORMAL)

    btn_stop.config(command=_stop_cmd)

    root.mainloop()


def _start(recorder, status_text, btn_start, btn_stop):
    try:
        recorder.start()
        status_text.set("Grabando… Dejá de escuchar cuando termines.")
        btn_start.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        btn_start.config(state=tk.NORMAL)
        btn_stop.config(state=tk.DISABLED)


def _run_transcribe(wav_path, status_text, transcript_area, btn_transcribe, root):
    if not wav_path or not Path(wav_path).exists():
        messagebox.showwarning("Aviso", "No hay grabación para transcribir.")
        return

    def do_transcribe():
        status_text.set("Transcribiendo… (puede tardar un poco)")
        root.update_idletasks()
        try:
            text = transcribe_file(str(wav_path), model_size="base", language="es")
            transcript_area.delete("1.0", tk.END)
            transcript_area.insert(tk.END, text or "(Sin texto detectado)")
            status_text.set("Listo. Podés guardar el transcript.")
        except Exception as e:
            transcript_area.delete("1.0", tk.END)
            transcript_area.insert(tk.END, f"Error: {e}")
            status_text.set("Error al transcribir.")
        finally:
            btn_transcribe.config(state=tk.NORMAL)

    btn_transcribe.config(state=tk.DISABLED)
    threading.Thread(target=do_transcribe, daemon=True).start()


def _save_transcript(transcript_area):
    text = transcript_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showinfo("Aviso", "No hay texto para guardar.")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Texto", "*.txt"), ("Markdown", "*.md"), ("Todos", "*.*")],
    )
    if path:
        Path(path).write_text(text, encoding="utf-8")
        messagebox.showinfo("Guardado", f"Guardado en: {path}")


if __name__ == "__main__":
    main()
