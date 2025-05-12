#!/usr/bin/env python3
"""
Image Processing Utilities for AI-PsychDoodle-Analyzer
"""

import base64
import io
import numpy as np
import cv2
from PIL import Image
from typing import Union, Tuple

def decode_base64_image(base64_str: str) -> np.ndarray:
    """
    Decode a base64 string into a numpy image array
    
    Args:
        base64_str: The base64 encoded image string
        
    Returns:
        Numpy array containing the image
    """
    # Strip the data URI prefix if present
    if base64_str.startswith('data:image'):
        base64_str = base64_str.split(',')[1]
    
    # Decode base64 string
    image_bytes = base64.b64decode(base64_str)
    
    # Convert to numpy array
    try:
        # Try using PIL first
        pil_image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(pil_image)
        
        # Convert RGB to BGR for OpenCV compatibility if needed
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            
        return image_array
    except Exception:
        # Fallback to OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image

def encode_base64_image(image: np.ndarray, format: str = 'jpeg') -> str:
    """
    Encode a numpy image array as a base64 string
    
    Args:
        image: The image as a numpy array
        format: The image format (default: 'jpeg')
        
    Returns:
        Base64 encoded image string
    """
    # Convert BGR to RGB if needed
    if len(image.shape) == 3 and image.shape[2] == 3:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = image
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image_rgb)
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    pil_image.save(buffer, format=format)
    
    # Encode as base64
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Add data URI prefix
    mime_type = f"image/{format}"
    data_uri = f"data:{mime_type};base64,{img_str}"
    
    return data_uri

def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Resize an image to the target size while preserving aspect ratio
    
    Args:
        image: The image to resize
        target_size: The target size as (width, height)
        
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    target_w, target_h = target_size
    
    # Calculate aspect ratios
    aspect_original = w / h
    aspect_target = target_w / target_h
    
    # Determine new dimensions
    if aspect_original > aspect_target:
        # Width-limited
        new_w = target_w
        new_h = int(target_w / aspect_original)
    else:
        # Height-limited
        new_h = target_h
        new_w = int(target_h * aspect_original)
    
    # Resize the image
    resized = cv2.resize(image, (new_w, new_h))
    
    # Create a black canvas of the target size
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    
    # Calculate position to paste the resized image
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    
    # Paste the resized image
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    
    return canvas

def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize an image for neural network input
    
    Args:
        image: The input image
        
    Returns:
        Normalized image with values in [0, 1]
    """
    # Ensure image is in floating point format
    normalized = image.astype(np.float32)
    
    # Scale to [0, 1]
    normalized /= 255.0
    
    return normalized

def apply_threshold(image: np.ndarray, threshold: int = 127) -> np.ndarray:
    """
    Apply thresholding to create a binary image
    
    Args:
        image: The input image
        threshold: Threshold value (default: 127)
        
    Returns:
        Binary image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Apply threshold
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    return binary

def extract_contours(image: np.ndarray) -> list:
    """
    Extract contours from a binary image
    
    Args:
        image: The input binary image
        
    Returns:
        List of contours
    """
    # Ensure image is binary
    if len(image.shape) == 3:
        binary = apply_threshold(image)
    else:
        binary = image
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def calculate_iou(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Calculate Intersection over Union (IoU) between two binary images
    
    Args:
        image1: First binary image
        image2: Second binary image
        
    Returns:
        IoU score (0.0 to 1.0)
    """
    # Ensure both images are binary
    binary1 = apply_threshold(image1) if len(image1.shape) == 3 else image1
    binary2 = apply_threshold(image2) if len(image2.shape) == 3 else image2
    
    # Calculate intersection and union
    intersection = cv2.bitwise_and(binary1, binary2)
    union = cv2.bitwise_or(binary1, binary2)
    
    # Calculate IoU
    intersection_area = np.count_nonzero(intersection)
    union_area = np.count_nonzero(union)
    
    # Avoid division by zero
    if union_area == 0:
        return 0.0
    
    iou = intersection_area / union_area
    
    return iou

def calculate_color_histogram(image: np.ndarray, bins: int = 8) -> np.ndarray:
    """
    Calculate color histogram for an image
    
    Args:
        image: The input image
        bins: Number of bins per channel
        
    Returns:
        Flattened color histogram
    """
    # Convert to RGB if needed
    if len(image.shape) == 3 and image.shape[2] == 3:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        rgb = image
    
    # Calculate histogram
    hist = cv2.calcHist([rgb], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    
    # Normalize
    cv2.normalize(hist, hist)
    
    # Flatten
    hist = hist.flatten()
    
    return hist

def detect_dominant_colors(image: np.ndarray, k: int = 5) -> list:
    """
    Detect dominant colors in an image using K-means clustering
    
    Args:
        image: The input image
        k: Number of dominant colors to detect
        
    Returns:
        List of (color, percentage) tuples
    """
    # Reshape image
    pixels = image.reshape(-1, 3)
    
    # Convert to float32
    pixels = np.float32(pixels)
    
    # Define criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    # Apply K-means
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert centers to uint8
    centers = np.uint8(centers)
    
    # Count labels
    unique_labels, counts = np.unique(labels, return_counts=True)
    
    # Calculate percentages
    total_pixels = len(pixels)
    
    # Create list of (color, percentage) tuples
    dominant_colors = []
    for i in range(len(unique_labels)):
        color = centers[unique_labels[i]].tolist()
        percentage = counts[i] / total_pixels
        dominant_colors.append((color, percentage))
    
    # Sort by percentage (descending)
    dominant_colors.sort(key=lambda x: x[1], reverse=True)
    
    return dominant_colors