# Course Enrollment System

A full-stack Course Enrollment Management System with a FastAPI backend and a modern HTML/CSS/JavaScript frontend.

## Overview

This system allows you to manage students, courses, and enrollments through a RESTful API and an intuitive web interface.

## Tech Stack

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLModel**: SQL database interactions with Python type hints
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation and settings management

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients, animations, and flexbox/grid layouts
- **Vanilla JavaScript**: No frameworks, pure ES6+ JavaScript
- **Fetch API**: For making HTTP requests to the backend

## Features

### Backend API

- 🎓 **Students Management**: Create, read, update, and delete students
- 📚 **Courses Management**: Create, read, update, and delete courses
- 📝 **Enrollments Management**: Enroll students in courses and manage enrollments
- 🔗 **Relationships**: View enrolled courses per student and enrolled students per course
- 📖 **Auto-generated Documentation**: Interactive API docs at `/docs`

### Frontend UI

- ✨ **Modern Design**: Clean, gradient-based design with smooth animations
- 📱 **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- 🎯 **Intuitive Navigation**: Tab-based interface for Students, Courses, and Enrollments
- 🔄 **Real-time Updates**: All changes are immediately reflected in the UI
- 💬 **Toast Notifications**: Success and error notifications for user actions
- 🔍 **Modal Dialogs**: Detailed views for students and courses with their relationships

## Project Structure

```
Course-Enrollment-Api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLModel data models
│   └── routers/
│       ├── __init__.py
│       ├── students.py      # Student endpoints
│       ├── courses.py       # Course endpoints
│       └── enrollments.py   # Enrollment endpoints
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Styling
│   └── app.js               # JavaScript functionality
├── pyproject.toml           # Python dependencies
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Modern web browser (Chrome, Firefox, Safari, or Edge)

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Course-Enrollment-Api
   ```

2. **Install dependencies**

   Using uv (recommended):

   ```bash
   uv pip install -e .
   ```

   Or using pip:

   ```bash
   pip install -e .
   ```

3. **Configure Database**

   Update the database connection string in `app/database.py`:

   ```python
   DATABASE_URL = "postgresql://username:password@localhost/dbname"
   ```

4. **Run the FastAPI server**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

5. **Access API Documentation**

   Open your browser and navigate to:

   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Enable CORS in Backend**

   Add CORS middleware to `app/main.py`:

   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # In production, specify your frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Run the Frontend**

   **Option 1: Using Python's HTTP Server**

   ```bash
   cd frontend
   python -m http.server 8080
   ```

   Then open `http://localhost:8080` in your browser.

   **Option 2: Using Node.js http-server**

   ```bash
   cd frontend
   npx http-server -p 8080
   ```

   **Option 3: Open Directly**
   Simply open `frontend/index.html` in your browser (may have CORS issues).

3. **Configure API URL (if needed)**

   If your backend is running on a different URL, update `API_BASE_URL` in `frontend/app.js`:

   ```javascript
   const API_BASE_URL = "http://your-backend-url:port";
   ```

## API Endpoints

### Students

- `POST /students/` - Create a new student
- `GET /students/` - Get all students
- `GET /students/{student_id}` - Get student by ID with enrolled courses
- `PATCH /students/{student_id}` - Update student details
- `DELETE /students/deleteStudentById/?student_id={id}` - Delete a student

### Courses

- `POST /courses/` - Create a new course
- `GET /courses/` - Get all courses
- `GET /courses/{course_id}` - Get course by ID with enrolled students
- `PATCH /courses/{course_id}` - Update course details
- `DELETE /courses/{course_id}` - Delete a course

### Enrollments

- `POST /enrollments/` - Enroll a student in a course
- `DELETE /enrollments/{student_id}/{course_id}` - Unenroll a student from a course

## Usage Guide

### Managing Students

1. Navigate to the "Students" tab
2. Click "+ Add Student" to create a new student
3. Fill in the name and email
4. Click on a student card to view their enrolled courses
5. Use the "Delete" button to remove a student

### Managing Courses

1. Navigate to the "Courses" tab
2. Click "+ Add Course" to create a new course
3. Fill in the course name and description
4. Click on a course card to view enrolled students
5. Use the "Delete" button to remove a course

### Managing Enrollments

1. Navigate to the "Enrollments" tab
2. Click "+ New Enrollment"
3. Select a student and course from the dropdowns
4. Choose an enrollment date
5. Click "Enroll" to create the enrollment
6. Use "Unenroll" to remove an enrollment

## Database Schema

### Student

- `id` (int, primary key)
- `name` (str)
- `email` (str)

### Course

- `id` (int, primary key)
- `name` (str)
- `description` (str)

### Enrollment

- `student_id` (int, foreign key)
- `course_id` (int, foreign key)
- `enrollment_date` (date)

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Backend Issues

**Issue**: Database connection errors

- **Solution**: Check your PostgreSQL connection string and ensure the database is running

**Issue**: Module not found errors

- **Solution**: Make sure all dependencies are installed with `uv pip install -e .` or `pip install -e .`

### Frontend Issues

**Issue**: "Failed to load students/courses/enrollments"

- **Solution**: Make sure your FastAPI backend is running and CORS is enabled

**Issue**: Changes not reflecting

- **Solution**: Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)

**Issue**: CORS errors in console

- **Solution**: Add the CORS middleware to your FastAPI app as shown in the setup section

## Future Enhancements

- 🔐 Authentication and authorization
- ✏️ Edit functionality for students and courses
- 🔍 Search and filter capabilities
- 📄 Pagination for large datasets
- 📊 Export data to CSV/PDF
- 📈 Advanced student/course analytics
- 🎨 Theme customization options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

---

Enjoy using the Course Enrollment System! 🎓
