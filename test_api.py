import requests
import json
import time

# API endpoint
url = "http://localhost:8000/comment"

# Test comments
test_comments = [
    "This product is amazing! I love it!",
    "Terrible experience, would not recommend to anyone",
    "It's okay, nothing special but works",
    "Best purchase I've ever made! Absolutely fantastic!",
    "Customer service was horrible and unhelpful",
    "The quality is average at best, nothing to write home about",
    "Absolutely love this! 5 stars! Perfect product!",
    "Disappointed with the performance, very poor quality",
    "Great value for money, very satisfied",
    "Waste of money, completely useless"
]

print("=" * 60)
print("SENTIMENT ANALYSIS API TEST")
print("=" * 60)

# Test each comment
for i, comment in enumerate(test_comments, 1):
    print(f"\nTest #{i}")
    print(f"Comment: {comment}")
    print("-" * 40)
    
    try:
        # Send request
        response = requests.post(
            url, 
            json={"comment": comment},
            headers={"Content-Type": "application/json"}
        )
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   Sentiment: {result['sentiment']}")
            print(f"   Rating: {result['rating']}/5")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Make sure the server is running on {url}")
        break
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("=" * 60)
    time.sleep(0.5)  # Small delay between requests

print("\n✅ Testing complete!")
