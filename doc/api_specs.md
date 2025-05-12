# AI-PsychDoodle-Analyzer API Specifications

This document outlines the API specifications for the AI-PsychDoodle-Analyzer system.

## Base URL

```
http://[server-address]:8000
```

## Authentication

Authentication is implemented using API keys passed in the `X-API-Key` header.

## Endpoints

### 1. Get Predefined Shapes

Retrieves a list of available predefined shapes that can be used in tracing exercises.

**Endpoint:** `GET /predefined-shapes`

**Response:**
```json
{
  "basic": ["triangle", "circle", "square"],
  "complex": ["star", "house", "tree", "person"],
  "emotional": ["heart", "smile", "frown"]
}
```

### 2. Shape Analysis

Analyzes a traced shape to determine the user's psychological state.

**Endpoint:** `POST /shape-analysis`

**Request Body:**
```json
{
  "original_image": "base64_encoded_image_string",
  "traced_image": "base64_encoded_image_string",
  "response_time": 2.5,
  "shape_type": "triangle"
}
```

**Response:**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "emotional_state": {
    "calm": 0.75,
    "anxious": 0.15,
    "focused": 0.65,
    "distracted": 0.25,
    "confident": 0.45,
    "hesitant": 0.35
  },
  "feedback": "Your drawing suggests a calm and balanced state of mind. You show remarkable focus and attention to detail.",
  "recommendation": "Try to maintain this balanced state through meditation or mindful activities."
}
```

### 3. Doodle Analysis

Transforms a doodle into a realistic image using GauGAN and analyzes the result.

**Endpoint:** `POST /doodle-analysis`

**Request Body:**
```json
{
  "doodle_image": "base64_encoded_image_string"
}
```

**Response:**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440001",
  "generated_image": "base64_encoded_image_string",
  "emotional_state": {
    "calm": 0.35,
    "anxious": 0.25,
    "energetic": 0.65,
    "melancholic": 0.15,
    "creative": 0.85,
    "logical": 0.25
  },
  "feedback": "Your drawing shows remarkable imagination and creativity. The vibrant elements suggest enthusiasm and high energy.",
  "recommendation": "Your imaginative state is perfect for artistic expression. Take advantage of this creative flow for problem-solving."
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `500 Internal Server Error`: Server-side error

Error response body:
```json
{
  "detail": "Error message explaining what went wrong"
}
```

## Data Models

### Shape Analysis Request

| Field | Type | Description |
|-------|------|-------------|
| original_image | string | Base64 encoded image of the original shape |
| traced_image | string | Base64 encoded image of the user's traced shape |
| response_time | number | Time taken to trace the shape (in seconds) |
| shape_type | string | Type of shape (e.g., "triangle", "circle", "square") |

### Shape Analysis Response

| Field | Type | Description |
|-------|------|-------------|
| analysis_id | string | Unique identifier for this analysis |
| emotional_state | object | Mapping of emotional states to scores (0.0-1.0) |
| feedback | string | Textual feedback based on the analysis |
| recommendation | string | Personalized recommendation based on the analysis |

### Doodle Analysis Request

| Field | Type | Description |
|-------|------|-------------|
| doodle_image | string | Base64 encoded doodle image |

### Doodle Analysis Response

| Field | Type | Description |
|-------|------|-------------|
| analysis_id | string | Unique identifier for this analysis |
| generated_image | string | Base64 encoded GauGAN-generated image |
| emotional_state | object | Mapping of emotional states to scores (0.0-1.0) |
| feedback | string | Textual feedback based on the analysis |
| recommendation | string | Personalized recommendation based on the analysis |

## Implementation Notes

### Base64 Image Encoding

Images should be encoded in base64 with the data URI prefix:
```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
```

### Response Time

Response time should be measured in seconds from when the original shape is first displayed to when the user completes their tracing.

### Emotional States

The specific emotional states returned may vary depending on the analysis type:

- **Shape Analysis** emotions may include: calm, anxious, excited, depressed, focused, distracted, confident, hesitant

- **Doodle Analysis** emotions may include: calm, anxious, energetic, melancholic, creative, logical, joyful, contemplative