from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import random

app = FastAPI(title="Sentiment Analysis API")

# Define request model
class CommentRequest(BaseModel):
    comment: str = Field(..., min_length=1, max_length=1000)

# Define response model for structured output
class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    rating: int = Field(..., ge=1, le=5)

@app.post("/comment", response_model=SentimentResponse)
async def analyze_sentiment(request: CommentRequest):
    """
    Analyze sentiment of a comment using keyword-based approach
    (Mock version - no API key required)
    """
    try:
        comment = request.comment.lower()
        
        # Define keyword dictionaries
        positive_words = {
            'amazing': 5, 'great': 4, 'excellent': 5, 'love': 5, 
            'best': 5, 'awesome': 5, 'fantastic': 5, 'good': 4,
            'wonderful': 5, 'perfect': 5, 'brilliant': 5, 'happy': 4,
            'satisfied': 4, 'impressed': 4, 'recommend': 4
        }
        
        negative_words = {
            'terrible': 1, 'horrible': 1, 'bad': 2, 'worst': 1,
            'hate': 1, 'awful': 1, 'disappointed': 2, 'poor': 2,
            'useless': 1, 'waste': 1, 'frustrating': 2, 'annoying': 2,
            'broken': 1, 'defective': 1, 'avoid': 2
        }
        
        neutral_indicators = ['okay', 'average', 'fine', 'decent', 
                             'moderate', 'acceptable', 'normal', 'standard']
        
        # Calculate sentiment scores
        positive_score = 0
        negative_score = 0
        
        # Check for positive words
        for word, score in positive_words.items():
            if word in comment:
                positive_score += score
        
        # Check for negative words
        for word, score in negative_words.items():
            if word in comment:
                negative_score += score
        
        # Check for neutral indicators
        is_neutral = any(word in comment for word in neutral_indicators)
        
        # Determine sentiment and rating
        if positive_score > negative_score and not is_neutral:
            # Positive sentiment
            rating = min(5, 3 + positive_score // 2)
            return SentimentResponse(sentiment="positive", rating=rating)
        
        elif negative_score > positive_score and not is_neutral:
            # Negative sentiment
            rating = max(1, 3 - negative_score // 2)
            return SentimentResponse(sentiment="negative", rating=rating)
        
        elif is_neutral or positive_score == negative_score:
            # Neutral or mixed sentiment
            if positive_score > 0 and negative_score > 0:
                # Mixed feelings - slightly leaning based on which is stronger
                if positive_score > negative_score:
                    return SentimentResponse(sentiment="positive", rating=3)
                elif negative_score > positive_score:
                    return SentimentResponse(sentiment="negative", rating=3)
                else:
                    return SentimentResponse(sentiment="neutral", rating=3)
            else:
                # Truly neutral
                return SentimentResponse(sentiment="neutral", rating=3)
        
        else:
            # Default case for comments without clear indicators
            # Use simple heuristics
            comment_length = len(comment.split())
            
            if comment_length < 3:
                # Very short comments - assume neutral
                return SentimentResponse(sentiment="neutral", rating=3)
            else:
                # Check for exclamation marks (often indicate strong emotion)
                if '!' in comment:
                    if any(word in comment for word in ['!', 'great', 'awesome']):
                        return SentimentResponse(sentiment="positive", rating=4)
                    else:
                        return SentimentResponse(sentiment="positive", rating=3)
                else:
                    return SentimentResponse(sentiment="neutral", rating=3)
                    
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing comment: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "Sentiment Analysis API is running (Mock Mode)",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "name": "Sentiment Analysis API",
        "endpoints": {
            "POST /comment": "Analyze sentiment of a comment",
            "GET /health": "Health check"
        },
        "mode": "Mock (no API key required)"
    }

# For debugging - print when app starts
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("Starting up Sentiment Analysis API...")
    print("Mode: MOCK (no OpenAI API key required)")
    print("Endpoint: POST /comment")
    print("=" * 50)
