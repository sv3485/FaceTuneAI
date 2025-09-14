"""
Music player module supporting both local files and Spotify integration
"""

import os
import random
import vlc
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import EMOTION_MUSIC_MAP, SPOTIFY_SETTINGS, LOCAL_MUSIC_SETTINGS

class MusicPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.current_track = None
        self.spotify_client = None
        self.setup_spotify()
        self.setup_local_music()

    def setup_spotify(self):
        """Initialize Spotify client if credentials are available"""
        try:
            self.spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
                scope='user-modify-playback-state user-read-playback-state'
            ))
        except Exception as e:
            print(f"Spotify setup failed: {str(e)}")
            self.spotify_client = None

    def setup_local_music(self):
        """Setup local music directory"""
        self.music_dir = LOCAL_MUSIC_SETTINGS['music_directory']
        self.supported_formats = LOCAL_MUSIC_SETTINGS['supported_formats']
        
        # Create music directory if it doesn't exist
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)

    def get_spotify_tracks(self, emotion):
        """Get tracks from Spotify based on emotion"""
        if not self.spotify_client:
            return None

        try:
            # Get music preferences for the emotion
            emotion_config = EMOTION_MUSIC_MAP.get(emotion, {})
            genres = emotion_config.get('genres', [])
            
            if not genres:
                return None

            # Search for tracks matching the emotion's genres
            results = self.spotify_client.search(
                q=f"genre:{random.choice(genres)}",
                type='track',
                limit=SPOTIFY_SETTINGS['limit'],
                market=SPOTIFY_SETTINGS['market']
            )

            tracks = results['tracks']['items']
            if tracks:
                return random.choice(tracks)
            return None

        except Exception as e:
            print(f"Error getting Spotify tracks: {str(e)}")
            return None

    def get_local_track(self, emotion):
        """Get a local track based on emotion"""
        try:
            # Get all music files from the music directory
            music_files = []
            for root, _, files in os.walk(self.music_dir):
                for file in files:
                    if any(file.lower().endswith(fmt) for fmt in self.supported_formats):
                        music_files.append(os.path.join(root, file))

            if music_files:
                return random.choice(music_files)
            return None

        except Exception as e:
            print(f"Error getting local track: {str(e)}")
            return None

    def play_track(self, track):
        """Play a track using VLC"""
        try:
            if isinstance(track, str):  # Local file
                media = self.instance.media_new(track)
            else:  # Spotify track
                media = self.instance.media_new(track['preview_url'])
            
            self.player.set_media(media)
            self.player.play()
            self.current_track = track
            return True

        except Exception as e:
            print(f"Error playing track: {str(e)}")
            return False

    def play_emotion_music(self, emotion):
        """Play music based on detected emotion"""
        if not emotion:
            return False

        # Try Spotify first, fall back to local files
        track = self.get_spotify_tracks(emotion)
        if not track:
            track = self.get_local_track(emotion)

        if track:
            return self.play_track(track)
        return False

    def stop(self):
        """Stop current playback"""
        self.player.stop()
        self.current_track = None

    def pause(self):
        """Pause current playback"""
        self.player.pause()

    def resume(self):
        """Resume current playback"""
        self.player.play()

    def get_current_track_info(self):
        """Get information about the currently playing track"""
        if not self.current_track:
            return None

        if isinstance(self.current_track, str):  # Local file
            return {
                'name': os.path.basename(self.current_track),
                'type': 'local'
            }
        else:  # Spotify track
            return {
                'name': self.current_track['name'],
                'artist': self.current_track['artists'][0]['name'],
                'type': 'spotify'
            } 