"""
Centralized model version constants.
Single source of truth for all model references across agents and APIs.

When upgrading models, change ONLY this file. All agents and API endpoints
import from here (with hardcoded fallback for Vercel serverless context).
"""

# Text generation model (used by all agents)
GEMINI_TEXT_MODEL = "gemini-3-pro-preview"

# Image generation models
IMAGEN_MODEL = "imagen-4.0-generate-001"
GEMINI_IMAGE_FALLBACK = "gemini-2.0-flash-exp-image-generation"

# API base URL
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
