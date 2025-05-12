#!/usr/bin/env python3
"""
Shape Analyzer Module for AI-PsychDoodle-Analyzer
Analyzes traced shapes to determine psychological state
"""

import os
import numpy as np
import cv2
from typing import Dict, Any, Tuple, List
from PIL import Image
import tensorflow as tf

class ShapeAnalyzer:
    """
    Analyzes traced shapes to determine psychological state based on 
    response time, shape accuracy, and drawing characteristics.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the shape analyzer model
        
        Args:
            model_path: Path to the pre-trained model (optional)
        """
        self.model_path = model_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "weights/shape_analyzer_model.h5"
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
            "calm", "anxious", "excited", "depressed", 
            "focused", "distracted", "confident", "hesitant"
        ]
        
        # Feedback templates
        self.feedback_templates = {
            "calm": [
                "Your drawing suggests a calm and balanced state of mind.",
                "Your steady hand indicates inner tranquility."
            ],
            "anxious": [
                "Your drawing suggests some underlying tension or anxiety.",
                "The way you traced the shape may indicate some nervousness."
            ],
            "excited": [
                "Your drawing suggests excitement and enthusiasm.",
                "Your energetic approach indicates high spirits."
            ],
            "depressed": [
                "Your drawing suggests some emotional heaviness.",
                "The pressure and pacing of your strokes may indicate low mood."
            ],
            "focused": [
                "Your drawing shows remarkable focus and attention to detail.",
                "Your precision indicates a highly concentrated state."
            ],
            "distracted": [
                "Your drawing suggests you might be experiencing some distractions.",
                "The irregularities may indicate divided attention."
            ],
            "confident": [
                "Your drawing shows confidence and decisiveness.",
                "Your bold strokes indicate self-assurance."
            ],
            "hesitant": [
                "Your drawing suggests some uncertainty or hesitation.",
                "The tentative strokes may indicate cautiousness."
            ]
        }
        
        # Recommendation templates
        self.recommendation_templates = {
            "calm": [
                "Try to maintain this balanced state through meditation or mindful activities.",
                "Your calm demeanor is an asset. Use it to tackle complex tasks today."
            ],
            "anxious": [
                "Consider taking deep breaths and practicing mindfulness to reduce tension.",
                "Focus on one task at a time to manage nervous energy."
            ],
            "excited": [
                "Channel your enthusiasm into creative endeavors.",
                "Use this energy for tasks requiring innovation and brainstorming."
            ],
            "depressed": [
                "Consider engaging in physical activity to boost your mood.",
                "Connect with others - social interactions can help lift your spirits."
            ],
            "focused": [
                "Your concentration is exceptional. Use it for demanding tasks.",
                "Remember to take occasional breaks to maintain this focus."
            ],
            "distracted": [
                "Try to minimize interruptions and create a dedicated work environment.",
                "Short meditation sessions might help improve your concentration."
            ],
            "confident": [
                "Your confidence serves you well. Consider tackling challenging tasks.",
                "Share your assurance with others who may need encouragement."
            ],
            "hesitant": [
                "Trust yourself more. Your careful approach has its own strengths.",
                "Breaking tasks into smaller steps might help reduce uncertainty."
            ]
        }
    
    def analyze(self, original_image: np.ndarray, traced_image: np.ndarray, 
                response_time: float, shape_type: str) -> Dict[str, float]:
        """
        Analyze the traced shape to determine psychological state
        
        Args:
            original_image: The original shape image
            traced_image: The user's traced shape image
            response_time: Time taken to trace the shape (seconds)
            shape_type: Type of shape (e.g., "triangle", "circle", "square")
            
        Returns:
            Dictionary mapping emotional states to scores (0.0-1.0)
        """
        # If the model is loaded, use it for prediction
        if self.model:
            return self._model_based_analysis(original_image, traced_image, response_time, shape_type)
        
        # Otherwise use heuristic analysis
        return self._heuristic_analysis(original_image, traced_image, response_time, shape_type)
    
    def _model_based_analysis(self, original_image: np.ndarray, traced_image: np.ndarray, 
                             response_time: float, shape_type: str) -> Dict[str, float]:
        """
        Use the trained model to analyze the traced shape
        """
        # Extract features
        features = self._extract_features(original_image, traced_image, response_time, shape_type)
        
        # Normalize features
        normalized_features = self._normalize_features(features)
        
        # Reshape for model input
        model_input = np.array([list(normalized_features.values())])
        
        # Get model predictions
        predictions = self.model.predict(model_input)[0]
        
        # Map predictions to emotion categories
        emotions = {category: float(score) for category, score in zip(self.emotion_categories, predictions)}
        
        return emotions
    
    def _heuristic_analysis(self, original_image: np.ndarray, traced_image: np.ndarray, 
                           response_time: float, shape_type: str) -> Dict[str, float]:
        """
        Use heuristics to analyze the traced shape when the model is not available
        """
        # Extract features
        features = self._extract_features(original_image, traced_image, response_time, shape_type)
        
        # Analyze overlap accuracy
        overlap_accuracy = features['overlap_percentage']
        
        # Analyze response time
        # Assume average tracing time is 2 seconds for baseline
        normalized_time = min(1.0, response_time / 2.0)
        
        # Analyze line steadiness
        line_steadiness = features['line_steadiness']
        
        # Analyze shape completion
        completion = features['completion_percentage']
        
        # Calculate emotional scores based on heuristics
        emotions = {
            "calm": 0.5 * (line_steadiness + min(1.0, 2.0 * (1.0 - abs(normalized_time - 0.5)))),
            "anxious": 0.5 * ((1.0 - line_steadiness) + max(0, normalized_time - 0.7)),
            "excited": 0.5 * ((1.0 - line_steadiness) + min(normalized_time, 0.7)),
            "depressed": 0.5 * ((1.0 - completion) + max(0, 1.5 * (normalized_time - 0.6))),
            "focused": 0.5 * (overlap_accuracy + line_steadiness),
            "distracted": 0.5 * ((1.0 - overlap_accuracy) + (1.0 - completion)),
            "confident": 0.5 * (min(normalized_time, 0.6) + completion * line_steadiness),
            "hesitant": 0.5 * (max(0, normalized_time - 0.6) + (1.0 - overlap_accuracy * completion))
        }
        
        # Normalize scores to sum to 1.0
        total = sum(emotions.values())
        emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    def _extract_features(self, original_image: np.ndarray, traced_image: np.ndarray, 
                         response_time: float, shape_type: str) -> Dict[str, float]:
        """
        Extract features from the traced shape
        """
        # Convert images to grayscale if they're not already
        if len(original_image.shape) > 2 and original_image.shape[2] > 1:
            original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        else:
            original_gray = original_image
            
        if len(traced_image.shape) > 2 and traced_image.shape[2] > 1:
            traced_gray = cv2.cvtColor(traced_image, cv2.COLOR_BGR2GRAY)
        else:
            traced_gray = traced_image
        
        # Threshold images to binary
        _, original_binary = cv2.threshold(original_gray, 127, 255, cv2.THRESH_BINARY)
        _, traced_binary = cv2.threshold(traced_gray, 127, 255, cv2.THRESH_BINARY)
        
        # Calculate overlap between original and traced shapes
        intersection = cv2.bitwise_and(original_binary, traced_binary)
        union = cv2.bitwise_or(original_binary, traced_binary)
        
        # Calculate overlap percentage (IoU - Intersection over Union)
        intersection_area = np.count_nonzero(intersection)
        union_area = np.count_nonzero(union)
        overlap_percentage = intersection_area / max(1, union_area)  # Avoid division by zero
        
        # Calculate completion percentage (how much of original shape is covered)
        original_area = np.count_nonzero(original_binary)
        completion_percentage = intersection_area / max(1, original_area)  # Avoid division by zero
        
        # Calculate line steadiness (using contour analysis)
        contours, _ = cv2.findContours(traced_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        line_steadiness = 0.5  # Default medium steadiness
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Calculate perimeter
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Approximate the contour
            approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)
            
            # Calculate steadiness based on approximation (more points = less steady)
            expected_points = {"triangle": 3, "square": 4, "rectangle": 4, "circle": 8}
            expected = expected_points.get(shape_type, 8)  # Default to circle if shape not recognized
            
            # Calculate how close the number of points is to expected
            points_ratio = min(len(approx), expected * 2) / (expected * 2)
            
            # More points than expected = less steady
            # Closer to expected number = steadier
            line_steadiness = 1.0 - points_ratio
        
        # Return extracted features
        return {
            "overlap_percentage": overlap_percentage,
            "completion_percentage": completion_percentage,
            "line_steadiness": line_steadiness,
            "response_time": response_time
        }
    
    def _normalize_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize feature values to range [0, 1]
        """
        # Define min/max ranges for each feature
        feature_ranges = {
            "overlap_percentage": (0.0, 1.0),
            "completion_percentage": (0.0, 1.0),
            "line_steadiness": (0.0, 1.0),
            "response_time": (0.5, 10.0)  # Assume 0.5s to 10s is the normal range
        }
        
        normalized = {}
        for feature, value in features.items():
            min_val, max_val = feature_ranges.get(feature, (0.0, 1.0))
            if feature == "response_time":
                # Normalize and invert (faster response_time -> higher value)
                normalized_value = 1.0 - min(1.0, max(0.0, (value - min_val) / (max_val - min_val)))
            else:
                normalized_value = min(1.0, max(0.0, (value - min_val) / (max_val - min_val)))
            normalized[feature] = normalized_value
            
        return normalized
    
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
        import random
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
        import random
        recommendation = random.choice(self.recommendation_templates[dominant_emotion])
        
        return recommendation