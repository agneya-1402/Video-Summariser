# Video Summarizer

A Flask-based web application that automatically generates text summaries from video content using speech recognition and natural language processing.

![Video Summarizer Interface](project-screenshot.png)

## Features

- Upload video files in various formats (MP4, AVI, MOV, MKV, WMV)
- Extract audio from video files
- Convert speech to text using Google's Speech Recognition
- Generate concise summaries using NLTK-based text summarization
- Clean, modern user interface
- Error handling and user feedback
- Automatic cleanup of temporary files

## Prerequisites

Before you begin, ensure you have installed:

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/agneya-1402/video-summariser.git
cd video-summarizer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Download required NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Project Structure
```
video-summarizer/
├── static/
│   └── style.css         # CSS styles
├── templates/
│   ├── index.html        # Main upload page
│   └── result.html       # Summary display page
├── temp_uploads/         # Temporary storage for uploads
├── app.py               # Main Flask application
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the interface to:
   - Click "Choose File" to select a video
   - Click "Summarize" to process the video
   - View the generated summary
   - Use "Summarize Another Video" to process more videos

## Dependencies

- Flask: Web framework
- moviepy: Video processing
- SpeechRecognition: Audio to text conversion
- NLTK: Text summarization
- Werkzeug: File handling and security

## Configuration

You can modify the following parameters in `app.py`:

- `UPLOAD_FOLDER`: Location for temporary files
- `ALLOWED_EXTENSIONS`: Supported video formats
- `summary_ratio`: Summary length (default: 0.3 or 30% of original text)

## Troubleshooting

### Common Issues

1. **Video Upload Fails**
   - Check if the video format is supported
   - Ensure the file size is not too large
   - Verify proper file permissions

2. **No Summary Generated**
   - Ensure the video has clear audio
   - Check if the speech is in English
   - Verify all NLTK data is downloaded

3. **Application Won't Start**
   - Confirm all dependencies are installed
   - Check if required ports are available
   - Verify Python version compatibility

### Error Messages

- "No file uploaded": No file was selected
- "Invalid file type": The uploaded file format is not supported
- "An error occurred while processing": General processing error

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Speech recognition powered by Google Speech-to-Text
- Text summarization using NLTK
- UI design inspired by modern web applications
