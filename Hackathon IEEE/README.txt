
# Audio Transcription and Summarization GUI

This Python project provides a graphical user interface (GUI) for selecting an audio file, transcribing its speech to text, summarizing the transcription, and exporting the summarized text as a `.txt` file. It supports various audio formats, including MP3, WAV, FLAC, OGG, and more.

## Features

- **Browse and select audio files**: Supports MP3, WAV, FLAC, OGG, M4A, and AAC formats.
- **Transcription**: Uses the Google Web Speech API to transcribe audio to text.
- **Summarization**: Uses the Hugging Face `transformers` library with GPU support (if available) to summarize the transcribed text.
- **Progress Tracking**: Displays progress bars for both transcription and summarization.
- **GPU Support**: Automatically uses GPU (if available) for faster summarization.
- **Export Summarized Text**: Exports the summarized text to a `.txt` file in the same directory as the input audio.
- **Custom Logo**: Displays a custom logo in the GUI and the window title bar.

## Installation

### Prerequisites

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) library (for handling images in the GUI)
- [Pydub](https://github.com/jiaaro/pydub) (for audio format conversion)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (for transcribing audio to text)
- [transformers](https://huggingface.co/transformers/) (for text summarization)
- [torch](https://pytorch.org/) (to enable GPU support)

### Install Dependencies

1. Install the required libraries by running:

    ```bash
    pip install pillow pydub SpeechRecognition transformers torch
    ```

2. You also need to install `ffmpeg` for the `pydub` library to handle audio format conversions. Download it [here](https://ffmpeg.org/download.html) and follow the installation instructions. Ensure `ffmpeg` is added to your system's PATH.

### Usage

1. **Clone or download the project:**

    ```bash
    git clone https://github.com/your-username/audio-transcription-gui.git
    cd audio-transcription-gui
    ```

2. **Prepare your logo:**

    - Place your logo image file (e.g., `logo.png`) in the project directory. The logo should be in `.png` format.
    - The logo will be displayed at the top of the GUI and set as the window’s title bar icon.

3. **Run the GUI:**

    In the project directory, run the main Python script:

    ```bash
    python AudioTranscriber.py
    ```

4. **Select an audio file:**

    - Click on the "Browse Audio File" button to choose an audio file from your system.
    - Supported formats include `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`, and `.aac`.

5. **Transcribe and summarize the audio:**

    - After selecting an audio file, the "Transcribe and Summarize" button will become enabled.
    - Click this button to start the transcription and summarization process.
    - A loading screen will appear with progress bars showing the progress of both the transcription and summarization.

6. **View and export summarized text:**

    - Once the transcription and summarization are complete, the summarized text will be displayed in the GUI.
    - The "Export Summarized Text" button will be enabled, allowing you to export the summarized text as a `.txt` file in the same directory as the audio file.

## Files and Directories

- **logo.png**: The logo of the app.
- **AudioTranscriber.py**: The main Python script that runs the GUI.

## Troubleshooting

- **Error: `ffmpeg` not found**: Ensure that `ffmpeg` is installed on your system and added to your PATH.
- **Pillow error with image resizing**: Ensure you are using a recent version of Pillow where the `Image.Resampling.LANCZOS` is available for resizing images.
- **CUDA/GPU not used**: Ensure that PyTorch detects your GPU. Run the following in Python to verify GPU availability:

    ```python
    import torch
    print(torch.cuda.is_available())
    ```

    This should return `True` if a GPU is available.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Key Updates:
- Added **summarization** of transcribed text using Hugging Face Transformers (`t5-small` model).
- **GPU support**: If a GPU is available, it will be automatically used for faster summarization.
- Enhanced **progress bars** for transcription and summarization, improving user experience.
- Simplified **export functionality** to save only the summarized text.
