"""
FlirtCraft Backend - Application Entry Point
Imports the configured FastAPI app from the modular structure
"""

import os
from app.main import app

# For uvicorn compatibility
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD_ENABLED", "false").lower() == "true"

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        access_log=True,
        log_level="debug" if os.getenv("DEBUG", "false").lower() == "true" else "info"
    )