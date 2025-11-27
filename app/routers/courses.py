from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

# Import our models and database session dependency
from app.database import get_session
from app.models import (
    Course,
    CourseBase,
    CourseCreate,
    CourseRead,
    CourseReadWithStudents,
)

# Initialize the APIRouter instance
router = APIRouter()

# --- 1. POST: Create a New Course ---
@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(*, session: Session = Depends(get_session), course: CourseCreate):
    """
    Creates a new course record.
    """
    db_course = Course.model_validate(course)
    
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    
    return db_course

# --- 2. GET: Read All Courses ---
@router.get("/", response_model=List[CourseRead])
def read_courses(*, session: Session = Depends(get_session)):
    """
    Retrieves a list of all courses.
    """
    courses = session.exec(select(Course)).all()
    return courses

# --- 3. GET: Read a Single Course by ID (with enrolled students) ---
@router.get("/{course_id}", response_model=CourseReadWithStudents)
def read_course(*, session: Session = Depends(get_session), course_id: int):
    """
    Retrieves a single course by ID, including the enrollment data.
    """
    course = session.get(Course, course_id)
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    return course

# --- 4. PATCH: Update a Course's Details ---
@router.patch("/{course_id}", response_model=CourseRead)
def update_course(
    *, 
    session: Session = Depends(get_session), 
    course_id: int, 
    course_update: CourseBase
):
    """
    Updates an existing course's details.
    """
    db_course = session.get(Course, course_id)
    
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = course_update.model_dump(exclude_unset=True)
    db_course.sqlmodel_update(update_data)
    
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    
    return db_course

# --- 5. DELETE: Delete a Course ---
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(*, session: Session = Depends(get_session), course_id: int):
    """
    Deletes a course record.
    """
    course = session.get(Course, course_id)
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    session.delete(course)
    session.commit()
    
    return {"ok": True}