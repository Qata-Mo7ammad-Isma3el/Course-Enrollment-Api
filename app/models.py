from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, create_engine


#! ---- Enrollment models
class EnrollmentBase(SQLModel):
    # These fields define the data structure for API input
    student_id: int
    course_id: int
    enrollment_date: datetime = Field(default_factory=datetime.now)


# --- Junction Table for Many-to-Many Relationship ---
class Enrollment(EnrollmentBase, table=True):
    """
    Junction table to link Students and Courses (Many-to-Many).
    It also holds extra data about the enrollment (enrollment_date).
    """

    student_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="student.id"
    )
    course_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="course.id"
    )


#! --- Course Model ---
class CourseBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    credits: int = Field(ge=1, le=8)  # Credits between 1 and 8


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


#! --- Student Model ---
class StudentBase(SQLModel):
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


# --- Pydantic Schemas for API (Inheriting from Base Models) ---
# These are used for creating new records via the API
class StudentCreate(StudentBase):
    pass


class CourseCreate(CourseBase):
    pass


# These are used for reading records (Pydantic validation for response)
# Including relationships is key for nested data in responses
class StudentRead(StudentBase):
    id: int


class CourseRead(CourseBase):
    id: int


# Simplified response models that include enrollment_date (no inheritance to avoid circular deps)
class CourseWithEnrollmentDate(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    credits: int
    enrollment_date: Optional[datetime] = None


class StudentWithEnrollmentDate(SQLModel):
    id: int
    first_name: str
    last_name: str
    email: str
    enrollment_date: Optional[datetime] = None


# Read schemas with relationships included (no inheritance to avoid circular deps)
class CourseReadWithStudents(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    credits: int
    students: List[StudentWithEnrollmentDate] = []


class StudentReadWithCourses(SQLModel):
    id: int
    first_name: str
    last_name: str
    email: str
    courses: List[CourseWithEnrollmentDate] = []
