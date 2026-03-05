"""
Start FastAPI Model Service
Run this to start the ML model API server
"""

import uvicorn
import sys

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Tridosha ML Model API Service")
    print("=" * 60)
    print("\nAPI will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "model_api:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
