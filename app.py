"""
Emotion-Based Music Player - Main Application
"""

import streamlit as st
import cv2
import time
from emotion_detector import EmotionDetector
from music_player import MusicPlayer
from config import SETTINGS

def main():
    st.title("Emotion-Based Music Player")
    st.write("Your music will adapt based on your emotions!")

    # Initialize components
    if 'detector' not in st.session_state:
        st.session_state.detector = EmotionDetector()
    if 'player' not in st.session_state:
        st.session_state.player = MusicPlayer()
    if 'is_playing' not in st.session_state:
        st.session_state.is_playing = False

    # Create columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Emotion Detection")
        # Start/Stop button
        if st.button("Start/Stop Camera"):
            st.session_state.is_playing = not st.session_state.is_playing

        # Display camera feed
        if st.session_state.is_playing:
            frame_placeholder = st.empty()
            emotion_placeholder = st.empty()
            
            while st.session_state.is_playing:
                frame = st.session_state.detector.get_current_emotion()
                if frame is not None:
                    frame_placeholder.image(frame, channels="BGR")
                    
                    # Get current emotion
                    emotion = st.session_state.detector.last_emotion
                    if emotion:
                        mapped_emotion = st.session_state.detector.get_emotion_mapping(emotion)
                        emotion_placeholder.write(f"Detected Emotion: {emotion} (Mapped to: {mapped_emotion})")
                        
                        # Play music based on emotion
                        st.session_state.player.play_emotion_music(mapped_emotion)
                
                time.sleep(0.1)  # Small delay to prevent high CPU usage

    with col2:
        st.header("Music Controls")
        if st.button("Stop Music"):
            st.session_state.player.stop()
        
        if st.button("Pause/Resume"):
            if st.session_state.player.player.is_playing():
                st.session_state.player.pause()
            else:
                st.session_state.player.resume()

        # Display current track info
        track_info = st.session_state.player.get_current_track_info()
        if track_info:
            st.write("Now Playing:")
            st.write(f"Title: {track_info['name']}")
            if track_info['type'] == 'spotify':
                st.write(f"Artist: {track_info['artist']}")

if __name__ == "__main__":
    main() 