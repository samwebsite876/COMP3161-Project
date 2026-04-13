CREATE DATABASE coursemanagement;
USE coursemanagement;

CREATE TABLE users (
    user_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'lecturer', 'student') NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    lecturer_id VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lecturer_id) REFERENCES users(user_id)
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id INT NOT NULL,
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE course_sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    order_num INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE course_content (
    content_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT,
    title VARCHAR(255),
    content_type VARCHAR(50), 
    content_url TEXT,
    uploaded_by VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES course_sections(section_id) ON DELETE CASCADE
);

CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    due_date DATE,
    max_score INT,
    created_by VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE discussion_replies (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    thread_id INT NOT NULL,
    content TEXT NOT NULL,
    author_id VARCHAR(20) NOT NULL,
    parent_reply_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (thread_id) REFERENCES discussion_threads(thread_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_reply_id) REFERENCES discussion_replies(reply_id) ON DELETE CASCADE
);

CREATE TABLE discussion_threads (
    thread_id INT AUTO_INCREMENT PRIMARY KEY,
    forum_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

CREATE TABLE forums (
    forum_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE calendar_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT,
    student_id VARCHAR(20),
    submission_text TEXT,
    submission_file TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade INT,
    graded_by VARCHAR(20),
    graded_at DATETIME,
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE
);


CREATE VIEW courses_50_plus AS
SELECT course_id, COUNT(student_id) AS total_students
FROM enrollments
GROUP BY course_id
HAVING COUNT(student_id) >= 50;

CREATE VIEW students_5_courses AS
SELECT student_id, COUNT(course_id) AS total_courses
FROM enrollments
GROUP BY student_id
HAVING COUNT(course_id) >= 5;

CREATE VIEW lecturers_3_courses AS
SELECT lecturer_id, COUNT(course_id) AS total_courses
FROM courses
GROUP BY lecturer_id
HAVING COUNT(course_id) >= 3;


CREATE VIEW top_10_courses AS
SELECT course_id, COUNT(student_id) AS total_students
FROM enrollments
GROUP BY course_id
ORDER BY total_students DESC
LIMIT 10;

CREATE VIEW top_10_students AS
SELECT s.student_id,
       AVG(g.grade) AS avg_grade
FROM submissions s
JOIN grades g ON s.submission_id = g.submission_id
GROUP BY s.student_id
ORDER BY avg_grade DESC
LIMIT 10;


