#!/usr/bin/env python3
"""
API Server for AI-PsychDoodle-Analyzer
Provides endpoints for drawing analysis and doodle transformation
"""

import os
import uuid
import json
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.shape_analyzer import ShapeAnalyzer
from models.drawing_analyzer import DrawingAnalyzer
from models.gaugan_adapter import GauGANAdapter
from utils.image_processing import decode_base64_image, encode_base64_image

app = FastAPI(title="AI-PsychDoodle-Analyzer API", 
             description="API for analyzing psychological state through drawings",
             version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
shape_analyzer = ShapeAnalyzer()
drawing_analyzer = DrawingAnalyzer()
gaugan_adapter = GauGANAdapter()

# API Models
class ShapeAnalysisRequest(BaseModel):
    original_image: str  # base64 encoded image
    traced_image: str    # base64 encoded image
    response_time: float # in seconds
    shape_type: str      # "triangle", "circle", "square", etc.

class ShapeAnalysisResponse(BaseModel):
    analysis_id: str
    emotional_state: Dict[str, float]  # Emotional states with scores
    feedback: str                      # Textual feedback
    recommendation: str                # Personalized recommendation

class DoodleAnalysisRequest(BaseModel):
    doodle_image: str  # base64 encoded doodle

class DoodleAnalysisResponse(BaseModel):
    analysis_id: str
    generated_image: str              # base64 encoded GauGAN-generated image
    emotional_state: Dict[str, float] # Emotional states with scores
    feedback: str                     # Textual feedback
    recommendation: str               # Personalized recommendation

@app.get("/")
async def root():
    return {"message": "Welcome to AI-PsychDoodle-Analyzer API", 
            "version": "1.0.0",
            "endpoints": ["/shape-analysis", "/doodle-analysis"]}

@app.post("/shape-analysis", response_model=ShapeAnalysisResponse)
async def analyze_shape(request: ShapeAnalysisRequest):
    """
    Analyze a traced shape to determine psychological state
    """
    try:
        # Decode images
        original_img = decode_base64_image(request.original_image)
        traced_img = decode_base64_image(request.traced_image)
        
        # Analyze the shape tracing
        analysis_results = shape_analyzer.analyze(
            original_image=original_img,
            traced_image=traced_img,
            response_time=request.response_time,
            shape_type=request.shape_type
        )
        
        # Get recommendations based on analysis
        feedback = shape_analyzer.generate_feedback(analysis_results)
        recommendation = shape_analyzer.generate_recommendation(analysis_results)
        
        return ShapeAnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            emotional_state=analysis_results,
            feedback=feedback,
            recommendation=recommendation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/doodle-analysis", response_model=DoodleAnalysisResponse)
async def analyze_doodle(request: DoodleAnalysisRequest):
    """
    Transform a doodle using GauGAN and analyze the result
    """
    try:
        # Decode doodle image
        doodle_img = decode_base64_image(request.doodle_image)
        
        # Generate image using GauGAN
        generated_img = gaugan_adapter.transform(doodle_img)
        
        # Analyze the generated image
        analysis_results = drawing_analyzer.analyze_image(generated_img)
        
        # Generate feedback and recommendations
        feedback = drawing_analyzer.generate_feedback(analysis_results)
        recommendation = drawing_analyzer.generate_recommendation(analysis_results)
        
        # Encode the generated image to base64
        encoded_image = encode_base64_image(generated_img)
        
        return DoodleAnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            generated_image=encoded_image,
            emotional_state=analysis_results,
            feedback=feedback,
            recommendation=recommendation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/predefined-shapes")
async def get_predefined_shapes():
    """
    Returns a list of available predefined shapes for tracing
    """
    shapes = {
        "basic": ["triangle", "circle", "square"],
        "complex": ["star", "house", "tree", "person"],
        "emotional": ["heart", "smile", "frown"]
    }
    return shapes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)