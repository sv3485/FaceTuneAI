# Emotion-Based Music Player

An intelligent music player that detects facial emotions through webcam and plays matching music automatically.

## Features

- Real-time facial emotion detection
- Automatic music selection based on detected emotions
- Streamlit-based user interface
- Support for both local music files and Spotify integration

## Setup Instructions

1. Install Python 3.8 or higher
2. Install VLC media player on your system
3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. For Spotify integration, create a `.env` file with your Spotify credentials:
   ```
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   ```

## Running the Application

1. Start the application:
   ```bash
   streamlit run app.py
   ```
2. Allow webcam access when prompted
3. The application will automatically detect your emotions and play matching music

## Project Structure

- `app.py`: Main application file
- `emotion_detector.py`: Emotion detection module
- `music_player.py`: Music playback module
- `config.py`: Configuration and emotion-music mapping
- `utils.py`: Utility functions

## Requirements

- Webcam
- Internet connection (for Spotify integration)
- VLC media player installed
- Python 3.8+

## License

MIT License 