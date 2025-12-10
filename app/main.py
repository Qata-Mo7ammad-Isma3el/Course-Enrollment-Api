from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

# Import database functions
from app.database import create_db_and_tables

# Import routers
from app.routers import students, courses, enrollments


# --- 1. Database Initialization on Startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI startup event handler.
    This function creates all defined tables in the PostgreSQL database.
    """
    # Startup code
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully.")
    yield
    # Shutdown code (if any)


app = FastAPI(title="Course Enrollment API", version="1.0.0", lifespan=lifespan)

# --- CORS Middleware Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # In production, replace with specific origins like ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Include Routers (API Endpoints) ---
# Uncomment and adjust these lines when the router files are created
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])


# --- Optional: A simple root endpoint ---
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Course Enrollment API. Go to /docs for API documentation."
    }
