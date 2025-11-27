from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

# Import our models and database session dependency
from app.database import get_session
from app.models import (
    Student,
    StudentCreate,
    StudentRead,
    StudentReadWithCourses,
    StudentBase,
)

# Initialize the APIRouter instance
router = APIRouter()

# --- 1. POST: Create a New Student ---
@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(*, session: Session = Depends(get_session), student: StudentCreate):
    """
    Creates a new student record in the database.
    Input data is validated against the StudentCreate Pydantic model.
    """
    # Create the SQLModel object from the Pydantic input
    db_student = Student.model_validate(student)
    
    # Add to the session and save to the database
    session.add(db_student)
    session.commit()
    session.refresh(db_student) # Retrieve the generated ID
    
    return db_student

# --- 2. GET: Read All Students ---
@router.get("/", response_model=List[StudentRead])
def read_students(*, session: Session = Depends(get_session)):
    """
    Retrieves a list of all students.
    """
    # Select all students using SQLModel's select statement
    students = session.exec(select(Student)).all()
    return students

# --- 3. GET: Read a Single Student by ID (with enrolled courses) ---
@router.get("/{student_id}", response_model=StudentReadWithCourses)
def read_student(*, session: Session = Depends(get_session), student_id: int):
    """
    Retrieves a single student by ID, including their enrollment data.
    """
    # SQLModel automatically handles the join when we use the StudentReadWithCourses model
    student = session.get(Student, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    return student

# --- 4. PATCH: Update a Student's Details ---
@router.patch("/{student_id}", response_model=StudentRead)
def update_student(
    *, 
    session: Session = Depends(get_session), 
    student_id: int, 
    student_update: StudentBase
):
    """
    Updates an existing student's details. Only fields provided are updated.
    """
    db_student = session.get(Student, student_id)
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get the dictionary of the Pydantic update model, excluding unset fields
    update_data = student_update.model_dump(exclude_unset=True)
    
    # Apply updates to the database model instance
    db_student.sqlmodel_update(update_data)
    
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    
    return db_student

# --- 5. DELETE: Delete a Student ---
@router.delete("/deleteStudentById/", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
        *,
        session: Session = Depends(get_session),
        student_id: Annotated[int, Query(ge=1, le=1000000)]
    ):
    """
    Deletes a student record. 
    Note: Deleting a student might require special handling for associated enrollment records 
    (cascading delete, which is handled by SQLModel/PostgreSQL configuration).
    """
    student = session.get(Student, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    session.delete(student)
    session.commit()
    
    return {"ok": True}