from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

app = FastAPI(
    title="Sentiment Analysis API",
    description="API for batch sentiment analysis of sentences",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class SentimentRequest(BaseModel):
    sentences: List[str]

class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

class SentimentResponse(BaseModel):
    results: List[SentimentResult]

# Comprehensive sentiment lexicons
HAPPY_WORDS = {
    'love', 'happy', 'great', 'awesome', 'excellent', 'good', 'wonderful',
    'fantastic', 'amazing', 'brilliant', 'perfect', 'joy', 'excited',
    'glad', 'pleased', 'delighted', 'enjoy', 'beautiful', 'best',
    'loving', 'like', 'nice', 'superb', 'outstanding', 'terrific',
    'fabulous', 'marvelous', 'splendid', 'magnificent', 'thrilled',
    'ecstatic', 'overjoyed', 'cheerful', 'positive', 'favorite',
    'appreciate', 'grateful', 'thankful', 'blessed', 'fortunate'
}

SAD_WORDS = {
    'sad', 'terrible', 'awful', 'horrible', 'bad', 'hate', 'worst',
    'disappointed', 'disappointing', 'poor', 'unhappy', 'miserable',
    'depressed', 'upset', 'angry', 'frustrated', 'annoyed', 'regret',
    'sorry', 'pain', 'hurt', 'suffer', 'difficult', 'hard', 'tough',
    'negative', 'awful', 'pathetic', 'useless', 'waste', 'problem',
    'issues', 'broken', 'failing', 'failed', 'loss', 'lose', 'missing'
}

# Negation words that flip sentiment
NEGATION_WORDS = {'not', "n't", 'never', 'no', 'none', 'neither', 'nor'}

# Intensifiers that strengthen sentiment
INTENSIFIERS = {
    'very', 'really', 'extremely', 'absolutely', 'completely',
    'totally', 'utterly', 'highly', 'deeply', 'terribly'
}

def preprocess_text(text: str) -> str:
    """Clean and normalize text."""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation but keep word boundaries
    text = re.sub(r'[^\w\s\']', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of a single sentence.
    Returns: 'happy', 'sad', or 'neutral'
    """
    if not text or not text.strip():
        return "neutral"
    
    original_text = text
    text = preprocess_text(text)
    words = text.split()
    
    # Check for explicit emotional statements
    if re.search(r'\b(i am|i\'m|i feel|feeling)\s+(so|very|really)?\s*(happy|glad|great|excited)\b', text):
        return "happy"
    if re.search(r'\b(i am|i\'m|i feel|feeling)\s+(so|very|really)?\s*(sad|depressed|upset|terrible)\b', text):
        return "sad"
    
    # Count sentiment words with context
    happy_score = 0
    sad_score = 0
    
    # Check for negation in the last 3 words before a sentiment word
    for i, word in enumerate(words):
        # Check if word is a sentiment word
        if word in HAPPY_WORDS:
            # Check for negation in preceding words
            negated = False
            intensified = False
            
            # Look at up to 3 words before
            start = max(0, i - 3)
            for j in range(start, i):
                if words[j] in NEGATION_WORDS:
                    negated = True
                if words[j] in INTENSIFIERS:
                    intensified = True
            
            if negated:
                sad_score += 2 if intensified else 1
            else:
                happy_score += 2 if intensified else 1
        
        elif word in SAD_WORDS:
            # Check for negation in preceding words
            negated = False
            intensified = False
            
            start = max(0, i - 3)
            for j in range(start, i):
                if words[j] in NEGATION_WORDS:
                    negated = True
                if words[j] in INTENSIFIERS:
                    intensified = True
            
            if negated:
                happy_score += 2 if intensified else 1
            else:
                sad_score += 2 if intensified else 1
    
    # Check for exclamation marks (often indicate strong emotion)
    if '!' in original_text:
        if happy_score > 0:
            happy_score += 1
        if sad_score > 0:
            sad_score += 1
    
    # Determine sentiment based on scores
    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
        return "sad"
    else:
        return "neutral"

@app.get("/")
async def root():
    return {
        "message": "Sentiment Analysis API",
        "usage": "POST /sentiment with JSON: {'sentences': ['text1', 'text2', ...]}",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/sentiment", response_model=SentimentResponse)
async def batch_sentiment_analysis(request: SentimentRequest):
    """
    Analyze sentiment for multiple sentences.
    Returns sentiment for each sentence in the same order as input.
    """
    if not request.sentences:
        raise HTTPException(status_code=400, detail="No sentences provided")
    
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    
    return SentimentResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
