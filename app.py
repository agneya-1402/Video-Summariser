from flask import Flask, render_template, request, redirect, url_for, flash
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import logging
import nltk
from werkzeug.utils import secure_filename
import time


try:
    nltk.download('punkt')
    nltk.download('stopwords')
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__) 

# upload settings
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_temp_files(files):
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
                logger.info(f"Cleaned up temporary file: {file}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file}: {e}")

def extract_audio(video_path):
    try:
        logger.info(f"Extracting audio from video: {video_path}")
        video = VideoFileClip(video_path)
        
        if video.audio is None:
            raise ValueError("No audio track found in video")
            
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp_audio.wav")
        video.audio.write_audiofile(audio_path, fps=16000, logger=None)
        video.close()
        
        logger.info("Audio extraction successful")
        return audio_path
    except Exception as e:
        logger.error(f"Error extracting audio: {e}")
        raise

def audio_to_text(audio_path):
    try:
        logger.info("Starting speech recognition")
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(audio_path) as source:
            logger.info("Reading audio file")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
            
        logger.info("Performing speech recognition")
        text = recognizer.recognize_google(audio)
        
        if not text:
            raise ValueError("No text was recognized from the audio")
            
        logger.info("Speech recognition successful")
        return text
    except sr.RequestError as e:
        logger.error(f"API error: {e}")
        raise
    except sr.UnknownValueError as e:
        logger.error("Speech recognition could not understand the audio")
        raise
    except Exception as e:
        logger.error(f"Error in speech recognition: {e}")
        raise

def summarize_text_nltk(text, summary_ratio=0.3):
    try:
        logger.info("Starting text summarization")
        
        # tokenize text
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(text.lower())
        
        # word frequencies
        word_freq = {}
        for word in words:
            if word.isalnum() and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
                
        # sentence scores
        sentences = sent_tokenize(text)
        sentence_scores = {}
        
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]
        
        # top sentences
        summary_length = max(1, int(len(sentences) * summary_ratio))
        summary_sentences = sorted(sentence_scores.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)[:summary_length]
        
        summary = ' '.join(sent for sent, score in sorted(
            summary_sentences, 
            key=lambda x: sentences.index(x[0])
        ))
        
        logger.info("Text summarization successful")
        return summary
    except Exception as e:
        logger.error(f"Error in text summarization: {e}")
        raise

def process_video(video_path):
    temp_files = [video_path]
    
    try:
        audio_path = extract_audio(video_path)
        temp_files.append(audio_path)
        
        text = audio_to_text(audio_path)
        
        summary = summarize_text_nltk(text)
        
        return summary
        
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise
    finally:
        clean_temp_files(temp_files)

@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        # check if file was uploaded
        if "file" not in request.files:
            flash("No file uploaded")
            return redirect(request.url)
            
        file = request.files["file"]
        
        # check if file was selected
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            try:
                # save uploaded file
                filename = secure_filename(file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(video_path)
                
                summary = process_video(video_path)
                
                return render_template("result.html", summary=summary)
                
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                flash("An error occurred while processing the video. Please try again.")
                return redirect(request.url)
        else:
            flash("Invalid file type. Please upload a video file.")
            return redirect(request.url)
            
    return render_template("index.html")

@app.errorhandler(Exception)
def handle_error(e):
    """Handle application errors"""
    logger.error(f"Application error: {e}")
    return render_template("result.html", 
                         summary="An error occurred while processing your request. Please try again.")

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
