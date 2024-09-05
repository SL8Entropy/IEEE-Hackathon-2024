import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import speech_recognition as sr
from pydub import AudioSegment
import os
import threading

def browse_file():
    # Open file dialog and allow the user to select an audio file
    filepath = filedialog.askopenfilename(
        title="Select an Audio File", 
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a *.aac")]
    )
    if filepath:
        file_label.config(text=f"Selected File: {os.path.basename(filepath)}")
        convert_button.config(state=tk.NORMAL)  # Enable the convert button
        global selected_file
        selected_file = filepath

def transcribe_audio(filepath):
    temp_wav_file = None  # To track if we created a temp wav file

    # Convert audio to wav if it's not in wav format
    if not filepath.endswith(".wav"):
        audio = AudioSegment.from_file(filepath)
        temp_wav_file = "converted_audio.wav"
        audio.export(temp_wav_file, format="wav")
        filepath = temp_wav_file

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the WAV file
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)

    # Recognize speech using Google Web Speech API
    try:
        text = recognizer.recognize_google(audio)
        result_label.config(text=f"Transcribed Text: {text}")
        global transcribed_text
        transcribed_text = text  # Store transcribed text
        export_button.config(state=tk.NORMAL)  # Enable export button
    except sr.UnknownValueError:
        result_label.config(text="Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        result_label.config(text=f"Could not request results from Google Web Speech API; {e}")
    
    # Remove the temporary wav file after transcription
    if temp_wav_file and os.path.exists(temp_wav_file):
        os.remove(temp_wav_file)
    
    # Hide loading screen
    hide_loading()

def start_transcription():
    if selected_file:
        show_loading()  # Show loading screen
        # Run transcription in a separate thread to avoid freezing the GUI
        threading.Thread(target=lambda: transcribe_audio(selected_file)).start()
    else:
        messagebox.showerror("Error", "Please select an audio file first.")

def show_loading():
    # Show loading screen
    loading_label.pack(pady=10)
    progress_bar.pack(pady=10)
    root.update_idletasks()  # Update GUI to reflect changes

def hide_loading():
    # Hide loading screen
    loading_label.pack_forget()
    progress_bar.pack_forget()
    root.update_idletasks()

def export_text():
    if transcribed_text:
        # Get the directory of the input file
        file_dir = os.path.dirname(selected_file)
        file_name = os.path.splitext(os.path.basename(selected_file))[0]
        export_path = os.path.join(file_dir, f"{file_name}_transcription.txt")
        
        # Save the transcribed text to a .txt file
        with open(export_path, "w") as f:
            f.write(transcribed_text)
        
        messagebox.showinfo("Success", f"Text exported successfully to {export_path}")
    else:
        messagebox.showerror("Error", "No transcription available to export.")

# Create GUI window
root = tk.Tk()
root.title("Audio Transcription")
root.geometry("400x400")  # Set window size
root.resizable(False, False)

selected_file = None
transcribed_text = None

# Add a file browsing button
browse_button = tk.Button(root, text="Browse Audio File", command=browse_file, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
browse_button.pack(pady=20)

# Label to show selected file
file_label = tk.Label(root, text="No file selected", font=("Arial", 10), fg="blue")
file_label.pack(pady=5)

# Add a convert button (disabled by default)
convert_button = tk.Button(root, text="Convert and Transcribe", command=start_transcription, bg="#2196F3", fg="white", font=("Arial", 12), width=20)
convert_button.pack(pady=20)
convert_button.config(state=tk.DISABLED)  # Initially disabled

# Loading screen elements (hidden by default)
loading_label = tk.Label(root, text="Transcribing, please wait...", font=("Arial", 10), fg="orange")
progress_bar = ttk.Progressbar(root, mode="indeterminate")

# Label to display transcription result
result_label = tk.Label(root, text="", wraplength=350, font=("Arial", 10), fg="green")
result_label.pack(pady=20)

# Add export button (disabled by default)
export_button = tk.Button(root, text="Export Transcribed Text", command=export_text, bg="#FF5722", fg="white", font=("Arial", 12), width=20)
export_button.pack(pady=20)
export_button.config(state=tk.DISABLED)  # Initially disabled

# Start the GUI main loop
root.mainloop()
