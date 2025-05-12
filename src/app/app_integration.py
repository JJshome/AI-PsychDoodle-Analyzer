#!/usr/bin/env python3
"""
Mobile App Integration for AI-PsychDoodle-Analyzer
Provides functions for integrating with mobile applications
"""
import os
import json
import requests
import base64
from typing import Dict, Any, List, Optional, Union
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PsychDoodleAppIntegration:
    """
    Integrates the AI-PsychDoodle-Analyzer with mobile applications
    """
    def __init__(self, api_url: str = None, api_key: str = None):
        """
        Initialize the app integration
        Args:
            api_url: URL of the AI-PsychDoodle-Analyzer API
            api_key: API key for authentication (if required)
        """
        self.api_url = api_url or "http://localhost:8000"
        self.api_key = api_key
        # Default timeout for API requests (seconds)
        self.timeout = 30
        # Default headers
        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key

    def get_predefined_shapes(self) -> Dict[str, List[str]]:
        """
        Get list of predefined shapes for tracing exercises
        Returns:
            Dictionary mapping shape categories to lists of shapes
        """
        try:
            response = requests.get(
                f"{self.api_url}/predefined-shapes",
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get predefined shapes: {e}")
            # Fallback to default shapes if API call fails
            return {
                "basic": ["triangle", "circle", "square"],
                "complex": ["star", "house", "tree"]
            }

    def analyze_traced_shape(self, original_image_base64: str, traced_image_base64: str,
                          response_time: float, shape_type: str) -> Dict[str, Any]:
        """
        Submit a traced shape for analysis
        Args:
            original_image_base64: Base64 encoded original shape image
            traced_image_base64: Base64 encoded traced shape image
            response_time: Time taken to trace the shape (seconds)
            shape_type: Type of shape (e.g., "triangle", "circle", "square")
        Returns:
            Analysis results
        """
        try:
            payload = {
                "original_image": original_image_base64,
                "traced_image": traced_image_base64,
                "response_time": response_time,
                "shape_type": shape_type
            }
            response = requests.post(
                f"{self.api_url}/analyze/traced-shape",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to analyze traced shape: {e}")
            # Return error message if API call fails
            return {
                "success": False,
                "error": str(e),
                "message": "Error analyzing traced shape"
            }

    def analyze_free_drawing(self, drawing_image_base64: str, drawing_time: float = None,
                          metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Submit a free drawing for analysis
        Args:
            drawing_image_base64: Base64 encoded drawing image
            drawing_time: Time spent on the drawing (seconds, optional)
            metadata: Additional metadata for the drawing (optional)
        Returns:
            Analysis results with GauGAN generated image
        """
        try:
            payload = {
                "drawing_image": drawing_image_base64,
                "drawing_time": drawing_time,
                "metadata": metadata or {}
            }
            response = requests.post(
                f"{self.api_url}/analyze/free-drawing",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to analyze free drawing: {e}")
            # Return error message if API call fails
            return {
                "success": False,
                "error": str(e),
                "message": "Error analyzing free drawing"
            }

    def get_feedback_suggestions(self, emotional_state: Dict[str, float]) -> List[Dict[str, str]]:
        """
        Get feedback suggestions based on emotional state
        Args:
            emotional_state: Dictionary of emotional states and their scores
                (e.g., {"anxiety": 0.7, "depression": 0.3, "happiness": 0.2})
        Returns:
            List of feedback suggestions
        """
        try:
            response = requests.post(
                f"{self.api_url}/feedback/suggestions",
                headers=self.headers,
                json={"emotional_state": emotional_state},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get feedback suggestions: {e}")
            # Fallback suggestions if API call fails
            return [
                {
                    "message": "Believe in the meaning of your existence.",
                    "category": "general"
                },
                {
                    "message": "A person who looks outward dreams, but a person who looks inward can awaken.",
                    "category": "inspiration"
                }
            ]

    def save_user_session(self, user_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save user session data
        Args:
            user_id: User identifier
            session_data: Session data to save
        Returns:
            Response with session ID
        """
        try:
            payload = {
                "user_id": user_id,
                "session_data": session_data,
                "timestamp": time.time()
            }
            response = requests.post(
                f"{self.api_url}/users/{user_id}/sessions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to save user session: {e}")
            # Return error message if API call fails
            return {
                "success": False,
                "error": str(e),
                "message": "Error saving user session"
            }

    def get_user_history(self, user_id: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        Get user session history
        Args:
            user_id: User identifier
            limit: Maximum number of sessions to return
            offset: Offset for pagination
        Returns:
            Dictionary with user sessions and statistics
        """
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            response = requests.get(
                f"{self.api_url}/users/{user_id}/history",
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user history: {e}")
            # Return error message if API call fails
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving user history"
            }

    def verify_connection(self) -> Dict[str, bool]:
        """
        Verify API connection
        Returns:
            Dictionary with connection status
        """
        try:
            response = requests.get(
                f"{self.api_url}/health",
                headers=self.headers,
                timeout=5  # Shorter timeout for health check
            )
            response.raise_for_status()
            return {"connected": True}
        except requests.exceptions.RequestException:
            return {"connected": False}


# Example usage
if __name__ == "__main__":
    # For testing during development
    app_integration = PsychDoodleAppIntegration()
    connection_status = app_integration.verify_connection()
    print(f"API connection status: {connection_status}")
    
    # Test getting predefined shapes
    shapes = app_integration.get_predefined_shapes()
    print(f"Available shapes: {shapes}")
