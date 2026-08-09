from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
import os
from dotenv import load_dotenv
from backend.routes import documents, search

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Guidely API")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# Middleware for Latency Logging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Simple heuristic to determine if the query hit cache
    # This could be refined based on actual cache hit data from vector store
    # Since we are using an in-memory vector store, latency is very low.
    cache_hit = "true" if process_time < 0.1 else "false"
    
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Cache-Hit"] = cache_hit
    
    logger.info(f"Path: {request.url.path} | Latency: {process_time:.4f}s | Cache Hit: {cache_hit}")
    return response

# Include Routers
app.include_router(documents.router)
app.include_router(search.router)

@app.get("/health", tags=["monitoring"])
async def health_check():
    return {"status": "ok"}

@app.get("/metrics", tags=["monitoring"])
async def metrics():
    # Placeholder for actual metrics logic
    return {
        "status": "ok",
        "message": "Metrics endpoint is active."
    }
