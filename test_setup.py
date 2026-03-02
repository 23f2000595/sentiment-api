import sys
print(f"Python path: {sys.executable}")
try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__} - OK")
except ImportError as e:
    print("FastAPI not found - ERROR")

try:
    import uvicorn
    print(f"Uvicorn found - OK")
except ImportError as e:
    print("Uvicorn not found - ERROR")
