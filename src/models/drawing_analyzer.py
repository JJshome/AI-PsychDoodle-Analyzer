#!/usr/bin/env python3
"""
Drawing Analyzer Module for AI-PsychDoodle-Analyzer
Analyzes free-form drawings and GauGAN-generated images
"""

import os
import numpy as np
import cv2
from typing import Dict, Any, Tuple, List
from PIL import Image
import tensorflow as tf
import random

class DrawingAnalyzer:
    """
    Analyzes free-form drawings and GauGAN-generated images to determine
    psychological state based on color usage, composition, and visual elements.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the drawing analyzer model
        
        Args:
            model_path: Path to the pre-trained model (optional)
        """
        self.model_path = model_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "weights/drawing_analyzer_model.h5"
        )
        
        # Check if model file exists, load if available
        self.model = None
        if os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
            except Exception as e:
                print(f"Warning: Could not load model from {self.model_path}: {e}")
                print("Using heuristic-based analysis instead.")
        
        # Emotion categories
        self.emotion_categories = [
            "calm", "anxious", "energetic", "melancholic", 
            "creative", "logical", "joyful", "contemplative"
        ]
        
        # Color-emotion associations (based on color psychology research)
        self.color_emotions = {
            "red": {"energetic": 0.8, "anxious": 0.6, "joyful": 0.4, "melancholic": 0.1},
            "blue": {"calm": 0.8, "contemplative": 0.7, "melancholic": 0.4, "anxious": 0.2},
            "green": {"calm": 0.7, "creative": 0.5, "logical": 0.4, "joyful": 0.4},
            "yellow": {"joyful": 0.8, "energetic": 0.7, "creative": 0.6, "anxious": 0.3},
            "purple": {"creative": 0.7, "contemplative": 0.6, "melancholic": 0.4, "calm": 0.3},
            "orange": {"energetic": 0.7, "joyful": 0.6, "creative": 0.5, "anxious": 0.3},
            "pink": {"joyful": 0.7, "creative": 0.5, "energetic": 0.4, "calm": 0.3},
            "brown": {"logical": 0.7, "contemplative": 0.6, "melancholic": 0.5, "calm": 0.4},
            "black": {"melancholic": 0.7, "contemplative": 0.6, "logical": 0.5, "anxious": 0.4},
            "white": {"logical": 0.6, "calm": 0.5, "contemplative": 0.4, "melancholic": 0.3},
            "gray": {"logical": 0.6, "contemplative": 0.5, "melancholic": 0.4, "calm": 0.3}
        }
        
        # Feedback templates
        self.feedback_templates = {
            "calm": [
                "Your drawing reflects a peaceful and balanced mindset.",
                "The composition shows inner harmony and tranquility."
            ],
            "anxious": [
                "Your drawing suggests some underlying tension or unease.",
                "The elements in your drawing may reflect some nervousness or worry."
            ],
            "energetic": [
                "Your drawing is full of vitality and dynamic energy.",
                "The vibrant elements suggest enthusiasm and high energy."
            ],
            "melancholic": [
                "Your drawing has a contemplative, somewhat somber quality.",
                "There's a thoughtful, introspective mood to your creation."
            ],
            "creative": [
                "Your drawing shows remarkable imagination and creativity.",
                "The unique elements reflect an innovative mindset."
            ],
            "logical": [
                "Your drawing shows structured thinking and methodical approach.",
                "The organized elements suggest analytical processing."
            ],
            "joyful": [
                "Your drawing radiates positivity and cheerfulness.",
                "The uplifting elements reflect a happy state of mind."
            ],
            "contemplative": [
                "Your drawing suggests deep thought and reflection.",
                "The thoughtful composition indicates philosophical consideration."
            ]
        }
        
        # Recommendation templates
        self.recommendation_templates = {
            "calm": [
                "Your peaceful mindset is ideal for meditation or reflective activities.",
                "Channel this tranquility into mindful practices or nature connection."
            ],
            "anxious": [
                "Try deep breathing exercises to help manage feelings of tension.",
                "Consider physical activity to release nervous energy."
            ],
            "energetic": [
                "Channel your abundant energy into creative or physical pursuits.",
                "This is a great time for brainstorming or starting new projects."
            ],
            "melancholic": [
                "Express your deeper feelings through journaling or art.",
                "Connect with a supportive friend to share what's on your mind."
            ],
            "creative": [
                "Your imaginative state is perfect for artistic expression.",
                "Take advantage of this creative flow for problem-solving."
            ],
            "logical": [
                "Your analytical mindset is ideal for organizing tasks or planning.",
                "Consider tackling complex problems requiring systematic thinking."
            ],
            "joyful": [
                "Share your positive energy with others who might need uplifting.",
                "Use this happy state to engage in fulfilling social activities."
            ],
            "contemplative": [
                "Your reflective state is perfect for journaling or deep reading.",
                "Take time for introspection and personal growth activities."
            ]
        }
    
    def analyze_image(self, image: np.ndarray) -> Dict[str, float]:
        """
        Analyze the image to determine psychological state
        
        Args:
            image: The image to analyze
            
        Returns:
            Dictionary mapping emotional states to scores (0.0-1.0)
        """
        # If the model is loaded, use it for prediction
        if self.model:
            return self._model_based_analysis(image)
        
        # Otherwise use heuristic analysis
        return self._heuristic_analysis(image)
    
    def _model_based_analysis(self, image: np.ndarray) -> Dict[str, float]:
        """
        Use the trained model to analyze the image
        """
        # Extract features
        features = self._extract_features(image)
        
        # Prepare model input (normalize and reshape)
        model_input = np.expand_dims(np.array(list(features.values())), axis=0)
        
        # Get model predictions
        predictions = self.model.predict(model_input)[0]
        
        # Map predictions to emotion categories
        emotions = {category: float(score) for category, score in zip(self.emotion_categories, predictions)}
        
        return emotions
    
    def _heuristic_analysis(self, image: np.ndarray) -> Dict[str, float]:
        """
        Use heuristics to analyze the image when the model is not available
        """
        # Extract features
        features = self._extract_features(image)
        
        # Initialize emotion scores
        emotions = {emotion: 0.0 for emotion in self.emotion_categories}
        
        # Calculate color-based emotions
        for color, percentage in features["color_distribution"].items():
            if color in self.color_emotions:
                for emotion, weight in self.color_emotions[color].items():
                    emotions[emotion] += percentage * weight
        
        # Adjust based on composition features
        # - High complexity can indicate creativity or anxiety
        complexity = features["complexity"]
        emotions["creative"] += complexity * 0.5
        emotions["anxious"] += complexity * 0.3
        
        # - Balance can indicate calmness or logical thinking
        balance = features["balance"]
        emotions["calm"] += balance * 0.5
        emotions["logical"] += balance * 0.4
        
        # - Contrast can indicate energy or melancholy
        contrast = features["contrast"]
        emotions["energetic"] += contrast * 0.4
        emotions["melancholic"] += (1 - contrast) * 0.3
        
        # - Brightness can indicate joy or contemplation
        brightness = features["brightness"]
        emotions["joyful"] += brightness * 0.6
        emotions["contemplative"] += (1 - brightness) * 0.5
        
        # Normalize scores to sum to 1.0
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        else:
            # Default to equal distribution if all scores are 0
            emotions = {k: 1.0/len(emotions) for k in emotions}
        
        return emotions
    
    def _extract_features(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extract visual features from the image
        """
        # Convert image to RGB if it's BGR
        if len(image.shape) == 3 and image.shape[2] == 3:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = image
        
        # Resize for consistent analysis
        resized = cv2.resize(rgb_image, (224, 224))
        
        # Extract color distribution
        color_distribution = self._analyze_colors(resized)
        
        # Calculate image complexity (edge density)
        gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        complexity = np.count_nonzero(edges) / (224 * 224)
        
        # Calculate balance (symmetry)
        left_half = gray[:, :112]
        right_half = cv2.flip(gray[:, 112:], 1)
        balance = 1.0 - (np.sum(np.abs(left_half - right_half)) / (112 * 224 * 255))
        
        # Calculate contrast
        contrast = np.std(gray) / 128.0  # Normalize by half of max intensity
        
        # Calculate brightness
        brightness = np.mean(gray) / 255.0
        
        return {
            "color_distribution": color_distribution,
            "complexity": complexity,
            "balance": balance,
            "contrast": contrast,
            "brightness": brightness
        }
    
    def _analyze_colors(self, image: np.ndarray) -> Dict[str, float]:
        """
        Analyze the color distribution in the image
        """
        # Define color ranges in HSV
        color_ranges = {
            "red1": ([0, 70, 50], [10, 255, 255]),
            "red2": ([170, 70, 50], [180, 255, 255]),  # Red wraps around in HSV
            "orange": ([11, 70, 50], [25, 255, 255]),
            "yellow": ([26, 70, 50], [35, 255, 255]),
            "green": ([36, 70, 50], [80, 255, 255]),
            "blue": ([81, 70, 50], [130, 255, 255]),
            "purple": ([131, 70, 50], [170, 255, 255]),
            "pink": ([0, 30, 180], [10, 150, 255]),
            "brown": ([10, 30, 50], [20, 150, 150]),
            "black": ([0, 0, 0], [180, 255, 50]),
            "white": ([0, 0, 200], [180, 30, 255]),
            "gray": ([0, 0, 50], [180, 30, 200])
        }
        
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # Get total pixel count
        total_pixels = image.shape[0] * image.shape[1]
        
        # Calculate color distribution
        color_distribution = {}
        
        # Process red as a special case (it wraps around in HSV)
        red1_mask = cv2.inRange(hsv, np.array(color_ranges["red1"][0]), np.array(color_ranges["red1"][1]))
        red2_mask = cv2.inRange(hsv, np.array(color_ranges["red2"][0]), np.array(color_ranges["red2"][1]))
        red_mask = cv2.bitwise_or(red1_mask, red2_mask)
        red_pixels = np.count_nonzero(red_mask)
        color_distribution["red"] = red_pixels / total_pixels
        
        # Process other colors
        for color, (lower, upper) in color_ranges.items():
            if color in ["red1", "red2"]:  # Skip red as it's handled separately
                continue
                
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            color_pixels = np.count_nonzero(mask)
            color_distribution[color] = color_pixels / total_pixels
        
        return color_distribution
    
    def generate_feedback(self, analysis: Dict[str, float]) -> str:
        """
        Generate feedback text based on analysis results
        
        Args:
            analysis: Dictionary mapping emotional states to scores (0.0-1.0)
            
        Returns:
            Feedback text
        """
        # Find the dominant emotion (highest score)
        dominant_emotion = max(analysis.items(), key=lambda x: x[1])[0]
        
        # Get a feedback template for the dominant emotion
        feedback = random.choice(self.feedback_templates[dominant_emotion])
        
        # Add additional insights based on secondary emotions
        secondary_emotions = sorted(analysis.items(), key=lambda x: x[1], reverse=True)[1:3]
        for emotion, score in secondary_emotions:
            if score > 0.2:  # Only consider significant secondary emotions
                feedback += f" {random.choice(self.feedback_templates[emotion]).lower()}"
        
        return feedback
    
    def generate_recommendation(self, analysis: Dict[str, float]) -> str:
        """
        Generate personalized recommendation based on analysis results
        
        Args:
            analysis: Dictionary mapping emotional states to scores (0.0-1.0)
            
        Returns:
            Recommendation text
        """
        # Find the dominant emotion (highest score)
        dominant_emotion = max(analysis.items(), key=lambda x: x[1])[0]
        
        # Get a recommendation template for the dominant emotion
        recommendation = random.choice(self.recommendation_templates[dominant_emotion])
        
        return recommendation