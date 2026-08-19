"""
Main FastAPI Application Entry Point
For AuditCompliance.cloud - Zero-Trust AI Compliance Platform
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.ingest import router as ingest_router

app = FastAPI(
    title="AuditCompliance.cloud API",
    description="Zero-Trust AI Compliance Platform - Continuous monitoring for violations",
    version="0.1.0-alpha",
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("AuditCompliance.cloud API starting...")
    # Initialize database connection
    # Initialize Redis connection
    # Initialize AI client
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("AuditCompliance.cloud API shutting down...")


# Include routers
app.include_router(ingest_router)


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to AuditCompliance.cloud API",
        "version": "0.1.0-alpha",
        "docs": "/docs",
        "status": "production-ready"
    }


# Health check for load balancers
@app.get("/healthz", tags=["monitoring"])
async def healthz():
    return {"status": "ok"}

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)