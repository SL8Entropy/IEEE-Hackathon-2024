Audio Transcription Application
This is a simple Python GUI application that transcribes audio files into text using OpenAI's Whisper model. The app provides functionality to transcribe audio files and export the transcribed text to a .txt file.

Features
Audio Transcription: Transcribes audio files in .wav, .mp3, and .flac formats using Whisper.
Progress Tracking: Displays progress for both transcription and correction.
Export: Allows users to export the transcribed text to a .txt file.
Reset: Clears the application state and resets the interface.
Requirements
Python 3.9+
Whisper (OpenAI)
PyTorch
Transformers (Hugging Face)
Tkinter (Standard Python library)
pydub (for audio format conversion)
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/audio-transcription-app.git
cd audio-transcription-app
Set up the environment: Create a Python virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate  # For Windows
Install dependencies: Run the following command to install the necessary libraries:

bash
Copy code
pip install -r requirements.txt
Additional Setup:

Install FFmpeg: Required for pydub to handle audio conversion.
Follow the FFmpeg installation guide to install FFmpeg and ensure it is in your system's PATH.
Usage
Run the application: After installing the dependencies, you can launch the application by running:

bash
Copy code
python audio_transcription_gui.py
Browse for an Audio File:

Click the "Browse Audio File" button and select an audio file (.wav, .mp3, or .flac).
Transcribe the Audio:

After selecting an audio file, click the "Transcribe" button to start the transcription process.
The app will show the progress and display the transcribed text.
Export the Transcribed Text:

Once transcription is complete, click the "Export Transcribed Text" button to save the text as a .txt file.
Reset the Application:

Click the "Reset" button to clear the interface and start over.
File Structure
plaintext
Copy code
audio-transcription-app/
│
├── audio_transcription_gui.py  # Main application script
├── requirements.txt            # List of required Python libraries
├── README.md                   # This README file
└── logo.ico                    # Application icon (optional)
Dependencies
Whisper: OpenAI’s Whisper model for transcription.
PyTorch: Backend used by Whisper for model inference.
Transformers: Hugging Face Transformers for handling pipeline loading.
pydub: Library for audio file conversion.
Tkinter: Standard library for building GUI applications.
Notes
CUDA Support: If a CUDA-enabled GPU is available, the application will use it to accelerate transcription. Otherwise, it will default to CPU.
Troubleshooting
FFmpeg Not Found: Ensure that FFmpeg is installed and added to your system's PATH.
Dependencies Missing: Run pip install -r requirements.txt to ensure all dependencies are installed.
Application Not Running: Check that your Python environment has the correct versions of the libraries listed in requirements.txt.
License
This project is licensed under the MIT License.