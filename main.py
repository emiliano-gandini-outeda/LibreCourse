from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from models import User, Course, Lesson, Note, Category
from routers import categories, auth_routers, courses
import uvicorn
import os

app = FastAPI(
    title="CourseTrackr API",
    description="A course management system API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_routers.router)
app.include_router(categories.router)
app.include_router(courses.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API is running smoothly"}

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to CourseTrackr API"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
