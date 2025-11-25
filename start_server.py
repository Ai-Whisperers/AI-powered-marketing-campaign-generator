"""
MAGA API Server Startup Script

This script properly configures the Python path and starts the FastAPI server.
"""

import sys
import os
from pathlib import Path

# Add the code directory to Python path
code_dir = Path(__file__).parent / "code"
sys.path.insert(0, str(code_dir))

# Now we can import and run uvicorn
import uvicorn

if __name__ == "__main__":
    print("=" * 80)
    print("MAGA API Server")
    print("=" * 80)
    print()
    print("Starting server...")
    print("URL: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print()
    print("Press CTRL+C to stop")
    print("=" * 80)
    print()
    
    # Run the server
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
