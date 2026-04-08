from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="api_user",
    password="$e@Rch876",
    database="coursemanagement",
    auth_plugin='mysql_native_password'
)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    userid = data.get('userid')
    password = data.get('password')
    role = data.get('role')

    if not userid or not password or not role:
        return jsonify({"error": "userid, password and role are required"}), 400

    if role not in ['admin', 'lecturer', 'student']:
        return jsonify({"error": "Invalid role"}), 400

    cursor = db.cursor()

    try:
        query = "INSERT INTO users (user_id, first_name, last_name, password, role, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (userid, 'First', 'Last', password, role, f"{userid}@uwi.edu"))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    userid = data.get('userid')
    password = data.get('password')

    if not userid or not password:
        return jsonify({"error": "userid and password are required"}), 400

    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
    cursor.execute(query, (userid, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user["user_id"],
                "userid": user["user_id"],
                "role": user["role"]
            }
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()

    course_code = data.get('course_code')
    course_name = data.get('course_name')
    lecturer_id = data.get('lecturer_id')
    created_by = data.get('created_by')

    if not course_code or not course_name or not created_by:
        return jsonify({"error": "course_code, course_name and created_by are required"}), 400

    cursor = db.cursor(dictionary=True)

    admin_check = "SELECT * FROM users WHERE user_id = %s AND role = 'admin'"
    cursor.execute(admin_check, (created_by,))
    admin = cursor.fetchone()

    if not admin:
        cursor.close()
        return jsonify({"error": "Only admins can create courses"}), 403

    if lecturer_id:
        lecturer_check = "SELECT * FROM users WHERE user_id = %s AND role = 'lecturer'"
        cursor.execute(lecturer_check, (lecturer_id,))
        lecturer = cursor.fetchone()

        if not lecturer:
            cursor.close()
            return jsonify({"error": "Assigned lecturer must be a lecturer"}), 400

    try:
        insert_query = """
            INSERT INTO courses (course_code, course_name, description, lecturer_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (course_code, course_name, '', lecturer_id))
        db.commit()
        return jsonify({"message": "Course created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


@app.route('/courses', methods=['GET'])
def get_all_courses():
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT c.course_id, c.course_code, c.course_name, u.user_id AS lecturer_name
        FROM courses c
        LEFT JOIN users u ON c.lecturer_id = u.user_id
    """
    cursor.execute(query)
    courses = cursor.fetchall()
    cursor.close()

    return jsonify(courses), 200


@app.route('/students/<student_id>/courses', methods=['GET'])
def get_student_courses(student_id):
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT c.course_id, c.course_code, c.course_name
        FROM enrollments cr
        JOIN courses c ON cr.course_id = c.course_id
        WHERE cr.student_id = %s
    """
    cursor.execute(query, (student_id,))
    courses = cursor.fetchall()
    cursor.close()

    return jsonify(courses), 200


@app.route('/lecturers/<lecturer_id>/courses', methods=['GET'])
def get_lecturer_courses(lecturer_id):
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT course_id, course_code, course_name
        FROM courses
        WHERE lecturer_id = %s
    """
    cursor.execute(query, (lecturer_id,))
    courses = cursor.fetchall()
    cursor.close()

    return jsonify(courses), 200


@app.route('/courses/<int:course_id>/register', methods=['POST'])
def register_for_course(course_id):
    data = request.get_json()
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    cursor = db.cursor(dictionary=True)

    student_check = "SELECT * FROM users WHERE user_id = %s AND role = 'student'"
    cursor.execute(student_check, (student_id,))
    student = cursor.fetchone()

    if not student:
        cursor.close()
        return jsonify({"error": "Only students can register for a course"}), 403

    course_check = "SELECT * FROM courses WHERE course_id = %s"
    cursor.execute(course_check, (course_id,))
    course = cursor.fetchone()

    if not course:
        cursor.close()
        return jsonify({"error": "Course not found"}), 404

    duplicate_check = """
        SELECT * FROM enrollments
        WHERE student_id = %s AND course_id = %s
    """
    cursor.execute(duplicate_check, (student_id, course_id))
    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return jsonify({"error": "Student already registered for this course"}), 400

    try:
        insert_query = """
            INSERT INTO enrollments (student_id, course_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (student_id, course_id))
        db.commit()
        return jsonify({"message": "Student registered for course successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()

@app.route('/sections', methods=['POST'])
def create_section():
    data = request.get_json()

    course_id = data.get('course_id')
    title = data.get('title')

    cursor = db.cursor()

    query = "INSERT INTO course_sections (course_id, title) VALUES (%s, %s)"
    cursor.execute(query, (course_id, title))
    db.commit()

    return jsonify({"message": "Section created"}), 201

@app.route('/content', methods=['POST'])
def add_content():
    data = request.get_json()

    section_id = data.get('section_id')
    title = data.get('title')
    content_type = data.get('content_type')
    content_url = data.get('content_url')
    uploaded_by = data.get('uploaded_by')

    cursor = db.cursor()

    query = """
        INSERT INTO course_content 
        (section_id, title, content_type, content_url, uploaded_by)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (section_id, title, content_type, content_url, uploaded_by))
    db.commit()

    return jsonify({"message": "Content added"}), 201

@app.route('/courses/<int:course_id>/content', methods=['GET'])
def get_course_content(course_id):
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT cs.title AS section, cc.title, cc.content_type, cc.content_url
        FROM course_sections cs
        JOIN course_content cc ON cs.section_id = cc.section_id
        WHERE cs.course_id = %s
    """

    cursor.execute(query, (course_id,))
    results = cursor.fetchall()

    return jsonify(results), 200

@app.route('/assignments', methods=['POST'])
def create_assignment():
    data = request.get_json()

    course_id = data.get('course_id')
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    created_by = data.get('created_by')

    cursor = db.cursor()

    query = """
        INSERT INTO assignments 
        (course_id, title, description, due_date, created_by)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (course_id, title, description, due_date, created_by))
    db.commit()

    return jsonify({"message": "Assignment created"}), 201

@app.route('/submit', methods=['POST'])
def submit_assignment():
    data = request.get_json()

    assignment_id = data.get('assignment_id')
    student_id = data.get('student_id')
    file_url = data.get('file_url')

    cursor = db.cursor()

    query = """
        INSERT INTO submissions 
        (assignment_id, student_id, submission_text, submission_file)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (assignment_id, student_id, 'Submission content', file_url))
    db.commit()

    return jsonify({"message": "Submitted"}), 201

@app.route('/grade', methods=['POST'])
def grade_assignment():
    data = request.get_json()

    submission_id = data.get('submission_id')
    grade = data.get('grade')
    graded_by = data.get('graded_by')

    # Validate input
    if not submission_id or grade is None or not graded_by:
        return jsonify({"error": "submission_id, grade, and graded_by are required"}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM submissions WHERE submission_id = %s", (submission_id,))
    submission = cursor.fetchone()

    if not submission:
        cursor.close()
        return jsonify({"error": "Submission not found"}), 404

    try:
        update_query = """
            UPDATE submissions
            SET grade = %s, graded_by = %s, graded_at = NOW()
            WHERE submission_id = %s
        """
        cursor.execute(update_query, (grade, graded_by, submission_id))
        db.commit()
        return jsonify({"message": f"Submission {submission_id} graded successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)