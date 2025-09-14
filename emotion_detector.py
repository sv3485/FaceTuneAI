"""
Emotion detection module using FER (Facial Expression Recognition)
"""

import cv2
import numpy as np
from fer import FER
import streamlit as st
from config import SETTINGS

class EmotionDetector:
    def __init__(self):
        """Initialize the emotion detector with FER model"""
        self.detector = FER(mtcnn=True)
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.cap = None
        self.last_emotion = None
        self.last_emotion_time = 0
        self.emotion_detection_interval = SETTINGS['emotion_detection_interval']
        self.confidence_threshold = SETTINGS['confidence_threshold']
        self.webcam_resolution = SETTINGS['webcam_resolution']

    def start_webcam(self):
        """Initialize webcam capture"""
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.webcam_resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.webcam_resolution[1])
        return self.cap.isOpened()

    def stop_webcam(self):
        """Release webcam resources"""
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()

    def get_frame(self):
        """Get current frame from webcam"""
        if self.cap is None or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def detect_emotion(self, frame):
        """
        Detect emotion in the given frame
        
        Args:
            frame: numpy array containing the image frame
            
        Returns:
            tuple: (dominant_emotion, confidence)
        """
        try:
            # Convert frame to RGB if it's in BGR
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                frame_rgb = frame
                
            # Detect emotions
            result = self.detector.detect_emotions(frame_rgb)
            
            if result:
                # Get the first face detected
                emotions = result[0]['emotions']
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])
                return dominant_emotion[0], dominant_emotion[1]
            
            return None, 0.0
            
        except Exception as e:
            st.error(f"Error in emotion detection: {str(e)}")
            return None, 0.0

    def get_current_emotion(self):
        """Get the current emotion from webcam feed"""
        frame = self.get_frame()
        if frame is None:
            return None

        # Only detect emotion at specified intervals
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        if (current_time - self.last_emotion_time) >= self.emotion_detection_interval:
            emotion, confidence = self.detect_emotion(frame)
            if emotion:
                self.last_emotion = emotion
                self.last_emotion_time = current_time

        return self.last_emotion

    def get_webcam_frame(self):
        """Get the current webcam frame for display"""
        frame = self.get_frame()
        if frame is None:
            return None
        
        # Add emotion text to frame if available
        if self.last_emotion:
            cv2.putText(
                frame,
                f"Emotion: {self.last_emotion}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        
        return frame

    def get_emotion_mapping(self, emotion):
        """
        Map detected emotion to music category
        
        Args:
            emotion: detected emotion string
            
        Returns:
            str: mapped emotion category
        """
        emotion_mapping = {
            'happy': 'happy',
            'sad': 'sad',
            'angry': 'energetic',
            'fear': 'calm',
            'surprise': 'energetic',
            'disgust': 'energetic',
            'neutral': 'neutral'
        }
        
        return emotion_mapping.get(emotion, 'neutral') 