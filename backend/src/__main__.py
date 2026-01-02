"""Entry point for running the server as a module."""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from server import app
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

