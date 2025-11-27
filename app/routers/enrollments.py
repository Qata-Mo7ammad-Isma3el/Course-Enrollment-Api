from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, and_

# Import our models and database session dependency
from app.database import get_session
from app.models import Enrollment, Student, Course

# Pydantic model for receiving enrollment data
class EnrollmentCreate(Enrollment):
    pass

# Initialize the APIRouter instance
router = APIRouter()

# --- 1. POST: Enroll a Student in a Course ---
@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def create_enrollment(*, session: Session = Depends(get_session), enrollment_data: EnrollmentCreate):
    """
    Creates a new enrollment record, linking a student to a course.
    Checks if student and course exist first.
    """
    # 1. Check if Student and Course exist
    student = session.get(Student, enrollment_data.student_id)
    course = session.get(Course, enrollment_data.course_id)

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {enrollment_data.student_id} not found.")
    
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with ID {enrollment_data.course_id} not found.")

    # 2. Check for existing enrollment (prevent duplicates)
    existing_enrollment = session.exec(
        select(Enrollment)
        .where(
            and_(
                Enrollment.student_id == enrollment_data.student_id, 
                Enrollment.course_id == enrollment_data.course_id
            )
        )
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Student is already enrolled in this course."
        )

    # 3. Create and save the new enrollment record
    db_enrollment = Enrollment.model_validate(enrollment_data)
    
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    
    return db_enrollment

# --- 2. DELETE: Un-enroll a Student from a Course ---
@router.delete("/{student_id}/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    *, 
    session: Session = Depends(get_session), 
    student_id: int, 
    course_id: int
):
    """
    Deletes a specific enrollment record (un-enrolls the student).
    """
    # Find the specific enrollment record using both primary keys
    enrollment = session.exec(
        select(Enrollment)
        .where(
            and_(
                Enrollment.student_id == student_id, 
                Enrollment.course_id == course_id
            )
        )
    ).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment record not found.")
        
    session.delete(enrollment)
    session.commit()
    
    return {"ok": True}