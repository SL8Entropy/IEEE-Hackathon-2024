
# Audio Transcription

This Python project provides a graphical user interface (GUI) that allows users to select an audio file, transcribe its speech to text, and export the transcribed text as a `.txt` file. It supports various audio formats, including MP3, WAV, FLAC, OGG, and more.

## Features

- Browse and select audio files of multiple formats.
- Convert the selected audio to `.wav` format if needed.
- Use Google Web Speech API to transcribe speech into text.
- Display a loading screen while the transcription is being processed.
- Export the transcribed text to a `.txt` file in the same directory as the input audio file.
- Includes a custom logo displayed in the GUI and the window title bar.

## Installation

### Prerequisites

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) library (for handling images in the GUI)
- [Pydub](https://github.com/jiaaro/pydub) (for audio format conversion)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (for transcribing audio to text)

### Install Dependencies

1. Install the required libraries by running:

    ```bash
    pip install pillow pydub SpeechRecognition
    ```

2. You also need to install `ffmpeg` for the `pydub` library to work properly for audio format conversions. Download it [here](https://ffmpeg.org/download.html) and follow the installation instructions. Make sure that `ffmpeg` is added to your system's PATH.

## Usage

1. **Clone or download the project:**

   ```bash
   git clone https://github.com/your-username/audio-transcription-gui.git
   cd audio-transcription-gui
   ```

2. **Prepare your logo:**

   - Place your logo image file (e.g., `your_logo.png`) in the project directory. The logo should be in `.png` format.
   - The logo will be displayed at the top of the GUI and set as the window’s title bar icon.

3. **Run the GUI:**

   In the project directory, run the main Python script:

   ```bash
   python AudioTranscriber.py
   ```
4. **Select an audio file:**

   - Click on the "Browse Audio File" button to choose an audio file from your system.
   - Supported formats include `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`, and `.aac`.

5. **Convert and transcribe the audio:**

   - After selecting an audio file, the "Convert and Transcribe" button will become enabled.
   - Click this button to start the transcription process. A loading screen will appear while the transcription is being processed.

6. **View and export transcribed text:**

   - Once the transcription is complete, the transcribed text will be displayed in the GUI.
   - The "Export Transcribed Text" button will be enabled, allowing you to export the text as a `.txt` file in the same directory as the audio file.

## Files and Directories

- **logo.png**: The logo of the app.
- **AudioTranscriber.py**: The main Python script that runs the GUI.


## Troubleshooting

- **Error: `ffmpeg` not found**: Make sure that `ffmpeg` is installed on your system and added to your PATH.
- **Pillow error with image resizing**: Ensure you are using a recent version of Pillow where the `Image.Resampling.LANCZOS` is available for resizing images.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
