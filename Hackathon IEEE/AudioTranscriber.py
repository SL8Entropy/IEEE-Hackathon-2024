import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import speech_recognition as sr
from pydub import AudioSegment
import os
import threading
from PIL import Image, ImageTk
from transformers import pipeline
import time
import torch
import math

# Global variables
selected_file = None
final_corrected_text = None

def browse_file():
    filepath = filedialog.askopenfilename(
        title="Select an Audio File", 
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a *.aac")]
    )
    if filepath:
        file_label.config(text=f"Selected File: {os.path.basename(filepath)}")
        convert_button.config(state=tk.NORMAL)
        global selected_file
        selected_file = filepath

def transcribe_and_correct(filepath):
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

    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk{i}.wav"
        chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            full_transcription.append(text)
            update_progress(i + 1, len(chunks), "Transcribing")  # Update the progress bar
            result_label.config(text=f"Transcribing chunk {i+1}/{len(chunks)}")
        except sr.UnknownValueError:
            full_transcription.append("[Unintelligible]")
        except sr.RequestError as e:
            full_transcription.append(f"[Error: {e}]")
        
        os.remove(chunk_filename)

    transcribed_text = ' '.join(full_transcription)

    # If the transcribed text is fewer than 20 words, display it, otherwise hide it.
    if len(transcribed_text.split()) <= 20:
        result_label.config(text=f"Transcribed Text: {transcribed_text}")
    else:
        result_label.config(text="Transcribed text is too long to display.")
    
    # Reset progress bar and prepare for grammar correction
    progress_bar['value'] = 0
    progress_label.config(text="Correcting grammar...")

    correct_grammar(transcribed_text)

    if temp_wav_file and os.path.exists(temp_wav_file):
        os.remove(temp_wav_file)

    hide_loading()


def correct_grammar(text):
    global final_corrected_text
    # Start a new thread for grammar correction
    threading.Thread(target=lambda: grammar_correction_task(text)).start()

def grammar_correction_task(text):
    global final_corrected_text

    device = 0 if torch.cuda.is_available() else -1  # Use GPU if available, otherwise CPU
    grammar_corrector = pipeline("text2text-generation", model="facebook/bart-large", device=device)

    # Simulate progress bar for grammar correction
    total_steps = 100
    for i in range(total_steps + 1):
        time.sleep(0.05)  # Simulate time delay for progress
        root.after(0, update_ui_progress, i)  # Update progress safely from the main thread

    # Perform grammar correction
    corrected = grammar_corrector(f"fix grammar: {text}", max_length=len(text), do_sample=False)
    final_corrected_text = corrected[0]['generated_text']

    # Display the corrected text
    root.after(0, display_corrected_text)  # Safely update UI from main thread

def update_ui_progress(i):
    progress_bar['value'] = i
    progress_label.config(text=f"Grammar correction in progress: {i}%")
    root.update_idletasks()

def display_corrected_text():
    if len(final_corrected_text.split()) <= 20:
        result_label.config(text=f"Corrected Text: {final_corrected_text}")
    else:
        result_label.config(text="Corrected text is too long to display.")
    export_button.config(state=tk.NORMAL)

def start_transcription_and_correction():
    if selected_file:
        convert_button.config(state=tk.DISABLED)  # Disable the button during processing
        show_loading()
        threading.Thread(target=lambda: transcribe_and_correct(selected_file)).start()
    else:
        messagebox.showerror("Error", "Please select an audio file first.")

def show_loading():
    loading_label.pack(pady=10)
    progress_bar.pack(pady=10)
    progress_label.pack(pady=5)
    root.update_idletasks()

def hide_loading():
    loading_label.pack_forget()
    progress_bar.pack_forget()
    progress_label.pack_forget()
    root.update_idletasks()

def update_progress(chunk_number, total_chunks, phase):
    progress_value = (chunk_number / total_chunks) * 100
    progress_bar['value'] = progress_value
    progress_label.config(text=f"{phase}... {int(progress_value)}%")
    root.update_idletasks()

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
    # Reset all UI elements and global variables
    file_label.config(text="No file selected")
    result_label.config(text="")
    progress_label.config(text="")
    progress_bar['value'] = 0
    convert_button.config(state=tk.DISABLED)
    export_button.config(state=tk.DISABLED)
    
    global selected_file, final_corrected_text
    selected_file = None
    final_corrected_text = None

# Create GUI window
root = tk.Tk()
root.title("Audio Transcription with Grammar Correction")
root.geometry("400x600")
root.resizable(False, False)

# Load and resize logo image (if available)
try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    root.iconphoto(False, logo_photo)
except FileNotFoundError:
    print("Logo image not found, skipping logo setup.")

browse_button = tk.Button(root, text="Browse Audio File", command=browse_file, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
browse_button.pack(pady=20)

file_label = tk.Label(root, text="No file selected", font=("Arial", 10), fg="blue")
file_label.pack(pady=5)

convert_button = tk.Button(root, text="Transcribe and Correct", command=start_transcription_and_correction, bg="#2196F3", fg="white", font=("Arial", 12), width=20)
convert_button.pack(pady=20)
convert_button.config(state=tk.DISABLED)

loading_label = tk.Label(root, text="Processing, please wait...", font=("Arial", 10), fg="orange")
progress_bar = ttk.Progressbar(root, mode="determinate", length=300)
progress_label = tk.Label(root, text="")  # Label for showing detailed progress

result_label = tk.Label(root, text="", wraplength=350, font=("Arial", 10), fg="green")
result_label.pack(pady=20)

export_button = tk.Button(root, text="Export Corrected Text", command=export_text, bg="#FF5722", fg="white", font=("Arial", 12), width=20)
export_button.pack(pady=20)
export_button.config(state=tk.DISABLED)

reset_button = tk.Button(root, text="Reset Program", command=reset_program, bg="#F44336", fg="white", font=("Arial", 12), width=20)
reset_button.pack(pady=20)

root.mainloop()
