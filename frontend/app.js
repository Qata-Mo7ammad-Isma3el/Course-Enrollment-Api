// API Base URL - Update this to match your FastAPI server
const API_BASE_URL = 'http://localhost:8000';

// State Management
let students = [];
let courses = [];
let enrollments = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeForms();
    loadAllData();
    setDefaultDate();
});

// Tab Navigation
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Remove active class from all buttons and contents
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            // Load data for the selected tab
            if (targetTab === 'students') {
                loadStudents();
            } else if (targetTab === 'courses') {
                loadCourses();
            } else if (targetTab === 'enrollments') {
                loadEnrollments();
            }
        });
    });
}

// Form Handlers
function initializeForms() {
    // Student Form
    document.getElementById('studentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createStudent();
    });

    // Course Form
    document.getElementById('courseForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createCourse();
    });

    // Enrollment Form
    document.getElementById('enrollmentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createEnrollment();
    });
}

// Load All Data
async function loadAllData() {
    await loadStudents();
    await loadCourses();
    await loadEnrollments();
}

// ===== STUDENTS =====

async function loadStudents() {
    try {
        const response = await fetch(`${API_BASE_URL}/students/`);
        if (!response.ok) throw new Error('Failed to load students');

        students = await response.json();
        renderStudents();
    } catch (error) {
        showToast('Error loading students: ' + error.message, 'error');
    }
}

function renderStudents() {
    const container = document.getElementById('studentsList');

    if (students.length === 0) {
        container.innerHTML = '<div class="empty-message">No students found. Add your first student!</div>';
        return;
    }

    container.innerHTML = students.map(student => `
        <div class="card" onclick="viewStudentDetails(${student.id})">
            <h3>👤 ${student.first_name} ${student.last_name}</h3>
            <p>📧 ${student.email}</p>
            <div class="card-actions" onclick="event.stopPropagation()">
                <button class="btn btn-danger" onclick="deleteStudent(${student.id})">Delete</button>
            </div>
        </div>
    `).join('');
} async function createStudent() {
    const first_name = document.getElementById('studentFirstName').value;
    const last_name = document.getElementById('studentLastName').value;
    const email = document.getElementById('studentEmail').value;

    try {
        const response = await fetch(`${API_BASE_URL}/students/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ first_name, last_name, email })
        });

        if (!response.ok) throw new Error('Failed to create student');

        showToast('Student created successfully!', 'success');
        hideAddStudentForm();
        await loadStudents();
        await loadEnrollments(); // Refresh enrollment dropdowns
    } catch (error) {
        showToast('Error creating student: ' + error.message, 'error');
    }
} async function deleteStudent(id) {
    if (!confirm('Are you sure you want to delete this student?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/students/deleteStudentById/?student_id=${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete student');

        showToast('Student deleted successfully!', 'success');
        await loadStudents();
        await loadEnrollments();
    } catch (error) {
        showToast('Error deleting student: ' + error.message, 'error');
    }
}

async function viewStudentDetails(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/students/${id}`);
        if (!response.ok) throw new Error('Failed to load student details');

        const student = await response.json();

        document.getElementById('modalStudentName').textContent = `${student.first_name} ${student.last_name}`;
        document.getElementById('modalStudentEmail').textContent = student.email; const coursesContainer = document.getElementById('modalStudentCourses');
        if (student.courses && student.courses.length > 0) {
            coursesContainer.innerHTML = student.courses.map(course =>
                `<span class="course-tag">${course.name}</span>`
            ).join('');
        } else {
            coursesContainer.innerHTML = '<p class="empty-message">Not enrolled in any courses</p>';
        }

        document.getElementById('studentModal').classList.add('show');
    } catch (error) {
        showToast('Error loading student details: ' + error.message, 'error');
    }
}

function closeStudentModal() {
    document.getElementById('studentModal').classList.remove('show');
}

function showAddStudentForm() {
    document.getElementById('addStudentForm').classList.remove('hidden');
    document.getElementById('studentForm').reset();
}

function hideAddStudentForm() {
    document.getElementById('addStudentForm').classList.add('hidden');
    document.getElementById('studentForm').reset();
}

// ===== COURSES =====

async function loadCourses() {
    try {
        const response = await fetch(`${API_BASE_URL}/courses/`);
        if (!response.ok) throw new Error('Failed to load courses');

        courses = await response.json();
        renderCourses();
    } catch (error) {
        showToast('Error loading courses: ' + error.message, 'error');
    }
}

function renderCourses() {
    const container = document.getElementById('coursesList');

    if (courses.length === 0) {
        container.innerHTML = '<div class="empty-message">No courses found. Add your first course!</div>';
        return;
    }

    container.innerHTML = courses.map(course => `
        <div class="card" onclick="viewCourseDetails(${course.id})">
            <h3>📖 ${course.name}</h3>
            <p>${course.description || 'No description'}</p>
            <p><strong>Credits:</strong> ${course.credits}</p>
            <div class="card-actions" onclick="event.stopPropagation()">
                <button class="btn btn-danger" onclick="deleteCourse(${course.id})">Delete</button>
            </div>
        </div>
    `).join('');
} async function createCourse() {
    const name = document.getElementById('courseName').value;
    const description = document.getElementById('courseDescription').value || null;
    const credits = parseInt(document.getElementById('courseCredits').value);

    try {
        const response = await fetch(`${API_BASE_URL}/courses/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, description, credits })
        });

        if (!response.ok) throw new Error('Failed to create course');

        showToast('Course created successfully!', 'success');
        hideAddCourseForm();
        await loadCourses();
        await loadEnrollments();
    } catch (error) {
        showToast('Error creating course: ' + error.message, 'error');
    }
} async function deleteCourse(id) {
    if (!confirm('Are you sure you want to delete this course?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/courses/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete course');

        showToast('Course deleted successfully!', 'success');
        await loadCourses();
        await loadEnrollments();
    } catch (error) {
        showToast('Error deleting course: ' + error.message, 'error');
    }
}

async function viewCourseDetails(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/courses/${id}`);
        if (!response.ok) throw new Error('Failed to load course details');

        const course = await response.json();

        document.getElementById('modalCourseName').textContent = course.name;
        document.getElementById('modalCourseDescription').textContent = course.description;

        const studentsContainer = document.getElementById('modalCourseStudents');
        if (course.students && course.students.length > 0) {
            studentsContainer.innerHTML = course.students.map(student =>
                `<span class="student-tag">${student.first_name} ${student.last_name}</span>`
            ).join('');
        } else {
            studentsContainer.innerHTML = '<p class="empty-message">No students enrolled</p>';
        }

        document.getElementById('courseModal').classList.add('show');
    } catch (error) {
        showToast('Error loading course details: ' + error.message, 'error');
    }
}

function closeCourseModal() {
    document.getElementById('courseModal').classList.remove('show');
}

function showAddCourseForm() {
    document.getElementById('addCourseForm').classList.remove('hidden');
    document.getElementById('courseForm').reset();
}

function hideAddCourseForm() {
    document.getElementById('addCourseForm').classList.add('hidden');
    document.getElementById('courseForm').reset();
}

// ===== ENROLLMENTS =====

async function loadEnrollments() {
    await loadStudents();
    await loadCourses();
    renderEnrollmentForm();
    renderEnrollmentsList();
}

function renderEnrollmentForm() {
    const studentSelect = document.getElementById('enrollmentStudent');
    const courseSelect = document.getElementById('enrollmentCourse');

    studentSelect.innerHTML = '<option value="">Select a student...</option>' +
        students.map(s => `<option value="${s.id}">${s.first_name} ${s.last_name}</option>`).join('');

    courseSelect.innerHTML = '<option value="">Select a course...</option>' +
        courses.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
} function renderEnrollmentsList() {
    const tbody = document.querySelector('#enrollmentsTable tbody');

    // Create a list of all enrollments from students
    const allEnrollments = [];
    students.forEach(student => {
        if (student.courses) {
            student.courses.forEach(course => {
                allEnrollments.push({
                    studentId: student.id,
                    studentName: `${student.first_name} ${student.last_name}`,
                    courseId: course.id,
                    courseName: course.name,
                    enrollmentDate: course.enrollment_date || 'N/A'
                });
            });
        }
    }); if (allEnrollments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-message">No enrollments found. Create your first enrollment!</td></tr>';
        return;
    }

    tbody.innerHTML = allEnrollments.map(enrollment => `
        <tr>
            <td>${enrollment.studentName}</td>
            <td>${enrollment.courseName}</td>
            <td>${enrollment.enrollmentDate}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteEnrollment(${enrollment.studentId}, ${enrollment.courseId})">
                    Unenroll
                </button>
            </td>
        </tr>
    `).join('');
}

async function createEnrollment() {
    const studentId = parseInt(document.getElementById('enrollmentStudent').value);
    const courseId = parseInt(document.getElementById('enrollmentCourse').value);
    const enrollmentDate = document.getElementById('enrollmentDate').value;

    if (!studentId || !courseId) {
        showToast('Please select both student and course', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/enrollments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                student_id: studentId,
                course_id: courseId,
                enrollment_date: enrollmentDate
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create enrollment');
        }

        showToast('Enrollment created successfully!', 'success');
        hideAddEnrollmentForm();
        await loadEnrollments();
    } catch (error) {
        showToast('Error creating enrollment: ' + error.message, 'error');
    }
}

async function deleteEnrollment(studentId, courseId) {
    if (!confirm('Are you sure you want to unenroll this student?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/enrollments/${studentId}/${courseId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete enrollment');

        showToast('Enrollment deleted successfully!', 'success');
        await loadEnrollments();
    } catch (error) {
        showToast('Error deleting enrollment: ' + error.message, 'error');
    }
}

function showAddEnrollmentForm() {
    document.getElementById('addEnrollmentForm').classList.remove('hidden');
    document.getElementById('enrollmentForm').reset();
    setDefaultDate();
    renderEnrollmentForm();
}

function hideAddEnrollmentForm() {
    document.getElementById('addEnrollmentForm').classList.add('hidden');
    document.getElementById('enrollmentForm').reset();
}

function setDefaultDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('enrollmentDate').value = today;
}

// ===== UTILITY FUNCTIONS =====

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Close modals when clicking outside
window.onclick = function (event) {
    const studentModal = document.getElementById('studentModal');
    const courseModal = document.getElementById('courseModal');

    if (event.target === studentModal) {
        closeStudentModal();
    }
    if (event.target === courseModal) {
        closeCourseModal();
    }
}
