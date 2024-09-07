import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk for the progress bar
import speech_recognition as sr
from pydub import AudioSegment
import os
import threading
from transformers import pipeline
import torch

# Global variables
selected_file = None
final_corrected_text = None

# GUI functions
def browse_file():
    global selected_file
    filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
    if filepath:
        selected_file = filepath
        file_label.config(text=f"Selected File: {os.path.basename(filepath)}")
        transcribe_button.config(state=tk.NORMAL)  # Enable the transcribe button once a file is selected
    else:
        file_label.config(text="No file selected")

def transcribe_and_correct():
    global selected_file
    if selected_file:
        transcribe_button.config(state=tk.DISABLED)  # Disable the transcribe button while processing
        status_label.config(text="Transcribing...")
        progress_bar['value'] = 0  # Reset the progress bar
        threading.Thread(target=lambda: transcribe_audio(selected_file)).start()
    else:
        messagebox.showerror("Error", "Please select a file before transcribing.")

def transcribe_audio(filepath):
    temp_wav_file = None
    # Convert to wav if needed
    if not filepath.endswith(".wav"):
        audio = AudioSegment.from_file(filepath)
        temp_wav_file = "converted_audio.wav"
        audio.export(temp_wav_file, format="wav")
        filepath = temp_wav_file

    audio = AudioSegment.from_wav(filepath)
    chunk_length_ms = 60000
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    recognizer = sr.Recognizer()
    full_transcription = []
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk{i}.wav"
        chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            full_transcription.append(text)
            update_status(f"Transcribing chunk {i+1}/{total_chunks}...")
        except sr.UnknownValueError:
            full_transcription.append("[Unintelligible]")
        except sr.RequestError as e:
            full_transcription.append(f"[Error: {e}]")
        
        os.remove(chunk_filename)

        # Update progress bar for transcription
        progress_bar['value'] = ((i + 1) / total_chunks) * 100
        root.update_idletasks()

    transcribed_text = ' '.join(full_transcription)

    # Show transcribed text only if it's 20 words or fewer
    if len(transcribed_text.split()) <= 20:
        transcribed_text_label.config(text=f"Transcribed Text: {transcribed_text}")
    else:
        transcribed_text_label.config(text="Transcribed text is too long to display.")

    update_status("Transcription complete. Correcting grammar...")
    
    # Reset progress bar for grammar correction
    progress_bar['value'] = 0
    root.update_idletasks()

    correct_grammar(transcribed_text)

    if temp_wav_file and os.path.exists(temp_wav_file):
        os.remove(temp_wav_file)

def correct_grammar(text):
    # Start a new thread for grammar correction
    threading.Thread(target=lambda: grammar_correction_task(text)).start()

def grammar_correction_task(text):
    global final_corrected_text

    device = 0 if torch.cuda.is_available() else -1  # Use GPU if available, otherwise CPU
    grammar_corrector = pipeline("text2text-generation", model="t5-large", device=device)

    # Simulate progress for grammar correction
    update_status("Correcting grammar...")
    corrected = grammar_corrector(f"fix grammar: {text}", max_length=len(text), do_sample=False)

    final_corrected_text = corrected[0]['generated_text']
    
    # Simulate grammar correction progress with a loop
    for i in range(100):
        progress_bar['value'] = i + 1
        root.update_idletasks()
        root.after(10)  # Wait a bit to show progress

    update_status("Grammar correction complete.")
    display_corrected_text()

def display_corrected_text():
    global final_corrected_text
    # Show corrected text only if it's 20 words or fewer
    if len(final_corrected_text.split()) <= 20:
        corrected_text_label.config(text=f"Corrected Text: {final_corrected_text}")
    else:
        corrected_text_label.config(text="Corrected text is too long to display.")
    
    export_button.config(state=tk.NORMAL)  # Enable export button after correction is done
    reset_button.config(state=tk.NORMAL)  # Enable reset button

def export_text():
    if final_corrected_text:
        file_dir = os.path.dirname(selected_file)
        file_name = os.path.splitext(os.path.basename(selected_file))[0]
        export_path = os.path.join(file_dir, f"{file_name}_corrected.txt")
        
        with open(export_path, "w") as f:
            f.write(final_corrected_text)
        
        messagebox.showinfo("Success", f"Corrected text exported successfully to {export_path}")
    else:
        messagebox.showerror("Error", "No corrected text available to export.")

def reset_program():
    global selected_file, final_corrected_text
    # Reset global variables
    selected_file = None
    final_corrected_text = None

    # Reset GUI components
    file_label.config(text="No file selected")
    transcribed_text_label.config(text="Transcribed text will appear here")
    corrected_text_label.config(text="Corrected text will appear here")
    status_label.config(text="Status: Idle")
    progress_bar['value'] = 0  # Reset progress bar

    # Disable buttons that should only be active at specific stages
    transcribe_button.config(state=tk.DISABLED)
    export_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.DISABLED)

def update_status(message):
    status_label.config(text=message)

# Create the main application window
root = tk.Tk()
root.title("Audio Transcription and Grammar Correction")
root.geometry("600x450")

# Set a custom window icon
logo_path = "logo.ico"  # Replace this with the actual path to your .ico logo file
root.iconbitmap(logo_path)

# Create and position widgets
browse_button = tk.Button(root, text="Browse Audio File", command=browse_file)
browse_button.pack(pady=10)

file_label = tk.Label(root, text="No file selected")
file_label.pack(pady=5)

transcribe_button = tk.Button(root, text="Transcribe and Correct", command=transcribe_and_correct)
transcribe_button.pack(pady=10)
transcribe_button.config(state=tk.DISABLED)  # Disable until file is selected

status_label = tk.Label(root, text="Status: Idle")
status_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

transcribed_text_label = tk.Label(root, text="Transcribed text will appear here")
transcribed_text_label.pack(pady=10)

corrected_text_label = tk.Label(root, text="Corrected text will appear here")
corrected_text_label.pack(pady=10)

export_button = tk.Button(root, text="Export Corrected Text", command=export_text)
export_button.pack(pady=10)
export_button.config(state=tk.DISABLED)  # Disable until correction is complete

reset_button = tk.Button(root, text="Reset", command=reset_program)
reset_button.pack(pady=10)
reset_button.config(state=tk.DISABLED)  # Disable until needed

# Start the Tkinter event loop
root.mainloop()
