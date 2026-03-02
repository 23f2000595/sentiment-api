# Sentiment Analysis API

A FastAPI-based sentiment analysis API that classifies sentences as "happy", "sad", or "neutral". Perfect for analyzing customer feedback, social media comments, or any text data.

## 🚀 Live Demo

The API is live at: `https://sentiment-api.onrender.com`

## 📋 Features

- Batch sentiment analysis of multiple sentences
- Returns results in the same order as input
- Three sentiment classifications: happy, sad, neutral
- Handles negations (e.g., "not happy" → sad)
- Recognizes intensifiers (e.g., "very happy" → stronger happy)
- Fast response times
- Comprehensive error handling

## 🛠️ Technology Stack

- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Render** - Cloud deployment

## 📚 API Endpoints

### 1. Root Endpoint
