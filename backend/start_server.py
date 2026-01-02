#!/usr/bin/env python3
"""Startup script for the backend server."""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

# Now import and run
if __name__ == "__main__":
    import uvicorn
    from server import app
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

