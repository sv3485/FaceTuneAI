"""
Configuration settings for the Emotion-Based Music Player
"""

# Emotion to music genre/playlist mapping
EMOTION_MUSIC_MAP = {
    'happy': {
        'genres': ['pop', 'dance', 'disco'],
        'mood': 'upbeat',
        'energy': 'high'
    },
    'sad': {
        'genres': ['indie', 'acoustic', 'piano'],
        'mood': 'melancholic',
        'energy': 'low'
    },
    'angry': {
        'genres': ['rock', 'metal', 'punk'],
        'mood': 'intense',
        'energy': 'high'
    },
    'neutral': {
        'genres': ['ambient', 'classical', 'jazz'],
        'mood': 'calm',
        'energy': 'medium'
    },
    'surprise': {
        'genres': ['electronic', 'experimental'],
        'mood': 'energetic',
        'energy': 'high'
    },
    'fear': {
        'genres': ['ambient', 'dark ambient'],
        'mood': 'tense',
        'energy': 'low'
    },
    'disgust': {
        'genres': ['industrial', 'experimental'],
        'mood': 'intense',
        'energy': 'medium'
    }
}

# Application settings
SETTINGS = {
    'emotion_detection_interval': 2,  # seconds between emotion checks
    'confidence_threshold': 0.5,      # minimum confidence for emotion detection
    'webcam_resolution': (640, 480),  # webcam resolution
    'music_switch_delay': 5,          # seconds to wait before switching songs
}

# Spotify settings
SPOTIFY_SETTINGS = {
    'market': 'US',
    'limit': 20,  # number of tracks to fetch per emotion
}

# Local music settings
LOCAL_MUSIC_SETTINGS = {
    'music_directory': 'music',  # directory containing local music files
    'supported_formats': ['.mp3', '.wav', '.ogg', '.flac']
} 