import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import whisper
import os
import threading
import torch
from pydub import AudioSegment

# Global variables
selected_file = None
transcribed_text = None  # Updated to hold the transcribed text

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

    # Initialize Whisper model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = whisper.load_model("base", device=device)
    
    # Transcribe audio
    transcription = model.transcribe(filepath)
    transcribed_text = transcription['text']

    # Show transcribed text only if it's 20 words or fewer
    if len(transcribed_text.split()) <= 20:
        transcribed_text_label.config(text=f"Transcribed Text: {transcribed_text}")
    else:
        transcribed_text_label.config(text="Transcribed text is too long to display.")
    print(transcribed_text)
    update_status("Transcription complete.")
    
    # Enable reset button once transcription is complete
    reset_button.config(state=tk.NORMAL)

    if temp_wav_file and os.path.exists(temp_wav_file):
        os.remove(temp_wav_file)

def export_text():
    global transcribed_text  # Now export transcribed_text
    if transcribed_text:
        file_dir = os.path.dirname(selected_file)
        file_name = os.path.splitext(os.path.basename(selected_file))[0]
        export_path = os.path.join(file_dir, f"{file_name}_transcribed.txt")
        
        with open(export_path, "w") as f:
            f.write(transcribed_text)
        
        messagebox.showinfo("Success", f"Transcribed text exported successfully to {export_path}")
    else:
        messagebox.showerror("Error", "No transcribed text available to export.")

def reset_program():
    global selected_file, transcribed_text
    # Reset global variables
    selected_file = None
    transcribed_text = None

    # Reset GUI components
    file_label.config(text="No file selected")
    transcribed_text_label.config(text="Transcribed text will appear here")
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
root.title("Audio Transcription")
root.geometry("600x450")

# Set a custom window icon
logo_path = "logo.ico"  # Replace this with the actual path to your .ico logo file
root.iconbitmap(logo_path)

# Create and position widgets
browse_button = tk.Button(root, text="Browse Audio File", command=browse_file)
browse_button.pack(pady=10)

file_label = tk.Label(root, text="No file selected")
file_label.pack(pady=5)

transcribe_button = tk.Button(root, text="Transcribe", command=transcribe_and_correct)
transcribe_button.pack(pady=10)
transcribe_button.config(state=tk.DISABLED)  # Disable until file is selected

status_label = tk.Label(root, text="Status: Idle")
status_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

transcribed_text_label = tk.Label(root, text="Transcribed text will appear here")
transcribed_text_label.pack(pady=10)

export_button = tk.Button(root, text="Export Transcribed Text", command=export_text)
export_button.pack(pady=10)
export_button.config(state=tk.DISABLED)  # Disable until transcription is complete

reset_button = tk.Button(root, text="Reset", command=reset_program)
reset_button.pack(pady=10)
reset_button.config(state=tk.DISABLED)  # Disable until needed

# Start the Tkinter event loop
root.mainloop()
