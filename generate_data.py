import random
import string
from datetime import datetime, timedelta
import hashlib
import sys

FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
    'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
    'Kenneth', 'Laura', 'Kevin', 'Sarah', 'Brian', 'Kimberly', 'George', 'Deborah',
    'Edward', 'Rebecca', 'Ronald', 'Stephanie', 'Timothy', 'Kathleen', 'Jason', 'Amy',
    'Jeffrey', 'Virginia', 'Ryan', 'Willow', 'Jacob', 'Abigail', 'Gary', 'Emily',
    'Nicholas', 'Catherine', 'Eric', 'Angela', 'Jonathan', 'Anna', 'Stephen', 'Ruth',
    'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Samantha',
    'Benjamin', 'Heather', 'Samuel', 'Christine', 'Gregory', 'Elizabeth', 'Frank', 'Emma',
    'Alexander', 'Megan', 'Raymond', 'Victoria', 'Patrick', 'Kayla', 'Jack', 'Chloe'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia',
    'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson',
    'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark',
    'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright',
    'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams', 'Nelson',
    'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts', 'Phillips',
    'Evans', 'Turner', 'Parker', 'Collins', 'Edwards', 'Stewart', 'Morris', 'Murphy',
    'Cook', 'Rogers', 'Morgan', 'Peterson', 'Cooper', 'Reed', 'Bailey', 'Bell'
]

NUM_STUDENTS = 100000
NUM_COURSES = 200
NUM_LECTURERS = 100
MIN_COURSES_PER_STUDENT = 3
MAX_COURSES_PER_STUDENT = 6
MIN_STUDENTS_PER_COURSE = 10
MAX_COURSES_PER_LECTURER = 5

def random_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def random_email(user_id):
    # Emails using uwi domain
    return f"{user_id}@uwi.edu"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def random_date(start_date, end_date):
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def random_string(length=20):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_sql_file():
    print("Starting data generation...")
    print(f"Target: {NUM_STUDENTS} students, {NUM_COURSES} courses")
    print("All emails will use @uwi.edu domain")
    
    try:
        with open('insert_data.sql', 'w', encoding='utf-8') as f:
            f.write("USE coursemanagement;\n\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            # ==================== USERS ====================
            print("\n[1/8] Generating users...")
            f.write("-- USERS\n")
            f.write("INSERT INTO users (user_id, first_name, last_name, password, role, email, created_at) VALUES\n")
            
            # Admin
            f.write("('admin', 'Admin', 'User', '" + hash_password("admin123") + "', 'admin', 'admin@uwi.edu', NOW()),\n")
            
            # Lecturers
            print("  - Generating lecturers...")
            lecturer_ids = []
            for i in range(1, NUM_LECTURERS + 1):
                first, last = random_name()
                user_id = f"lec_{i:03d}"
                lecturer_ids.append(user_id)
                email = random_email(user_id)
                f.write(f"('{user_id}', '{first}', '{last}', '" + hash_password(f"lec{i}") + f"', 'lecturer', '{email}', NOW())")
                if i < NUM_LECTURERS:
                    f.write(",\n")
            f.write(";\n\n")
            print(f"    ✓ Generated {NUM_LECTURERS} lecturers")
            
            # Students - generate ALL 100,000
            print("  - Generating students (this will take a few minutes)...")
            student_ids = []
            batch_size = 10000
            
            # Write first batch header
            first_batch = True
            
            for batch_start in range(0, NUM_STUDENTS, batch_size):
                batch_end = min(batch_start + batch_size, NUM_STUDENTS)
                
                # Write INSERT header for this batch
                if not first_batch:
                    f.write("INSERT INTO users (user_id, first_name, last_name, password, role, email, created_at) VALUES\n")
                
                for i in range(batch_start + 1, batch_end + 1):
                    first, last = random_name()
                    user_id = f"stu_{i:06d}"
                    student_ids.append(user_id)
                    email = random_email(user_id)
                    f.write(f"('{user_id}', '{first}', '{last}', '" + hash_password(f"stu{i}") + f"', 'student', '{email}', NOW())")
                    
                    if i < batch_end:
                        f.write(",\n")
                
                f.write(";\n\n")
                print(f"    ✓ Generated {batch_end:,} / {NUM_STUDENTS:,} students")
                first_batch = False
                
                # Flush to disk to save memory
                f.flush()
            
            print(f"  ✓ Total students generated: {len(student_ids):,}")
            
            # ==================== COURSES ====================
            print("\n[2/8] Generating courses...")
            f.write("-- COURSES\n")
            f.write("INSERT INTO courses (course_code, course_name, description, lecturer_id, created_at) VALUES\n")
            
            courses = []
            course_names = ['Programming', 'Data Structures', 'Algorithms', 'Databases', 'Web Development', 
                           'Computer Networks', 'Operating Systems', 'Artificial Intelligence', 'Machine Learning', 
                           'Cybersecurity', 'Cloud Computing', 'Mobile Development', 'Game Development', 
                           'Computer Graphics', 'Software Engineering', 'Compilers', 'Distributed Systems',
                           'Human Computer Interaction', 'Information Security', 'Data Mining']
            
            courses_per_lecturer = [0] * NUM_LECTURERS
            for i in range(1, NUM_COURSES + 1):
                min_courses = min(courses_per_lecturer)
                available = [j for j, count in enumerate(courses_per_lecturer) if count == min_courses and count < MAX_COURSES_PER_LECTURER]
                if not available:
                    available = [j for j, count in enumerate(courses_per_lecturer) if count < MAX_COURSES_PER_LECTURER]
                lecturer_idx = random.choice(available)
                courses_per_lecturer[lecturer_idx] += 1
                
                course_code = f"CS{i:03d}"
                courses.append(course_code)
                course_name = f"{random.choice(course_names)} {i}"
                description = f"Comprehensive course covering {course_name}"
                lecturer_id = lecturer_ids[lecturer_idx]
                
                f.write(f"('{course_code}', '{course_name}', '{description}', '{lecturer_id}', NOW())")
                if i < NUM_COURSES:
                    f.write(",\n")
            f.write(";\n\n")
            print(f"  ✓ Generated {NUM_COURSES} courses")
            
            # ==================== ENROLLMENTS ====================
            print("\n[3/8] Creating enrollments...")
            f.write("-- ENROLLMENTS\n")
            f.write("INSERT INTO enrollments (student_id, course_id, enrolled_at) VALUES\n")
            
            course_ids = {code: i+1 for i, code in enumerate(courses)}
            enrollments = []
            
            # Each course gets minimum students
            print("  - Assigning minimum students per course...")
            student_idx = 0
            for course_code in courses:
                for _ in range(MIN_STUDENTS_PER_COURSE):
                    enrollments.append((student_ids[student_idx % len(student_ids)], course_code))
                    student_idx += 1
            
            # Each student gets minimum courses
            print("  - Ensuring minimum courses per student...")
            student_course_count = {}
            for student_id, course_code in enrollments:
                student_course_count[student_id] = student_course_count.get(student_id, 0) + 1
            
            for student_id in student_ids:
                current = student_course_count.get(student_id, 0)
                needed = MIN_COURSES_PER_STUDENT - current
                if needed > 0:
                    enrolled = {c for s, c in enrollments if s == student_id}
                    available = [c for c in courses if c not in enrolled]
                    for i in range(min(needed, len(available))):
                        enrollments.append((student_id, available[i]))
            
            print(f"  ✓ Created {len(enrollments):,} enrollments")
            
            # Write enrollments in batches
            print("  - Writing enrollments to SQL...")
            for idx, (student_id, course_code) in enumerate(enrollments):
                f.write(f"('{student_id}', {course_ids[course_code]}, NOW())")
                if idx < len(enrollments) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            f.flush()
            
            # ==================== CALENDAR EVENTS ====================
            print("\n[4/8] Generating calendar events...")
            f.write("-- CALENDAR EVENTS\n")
            f.write("INSERT INTO calendar_events (course_id, title, description, event_date, created_at) VALUES\n")
            
            start_date = datetime(2024, 1, 1)
            end_date = datetime(2024, 12, 31)
            events = []
            for i, course_code in enumerate(courses[:100], 1):
                for j in range(random.randint(3, 6)):
                    event_date = random_date(start_date, end_date)
                    title = f"{course_code} - {'Lecture' if j % 2 == 0 else 'Lab'} Session {j+1}"
                    description = f"Regular class meeting for {course_code}"
                    events.append((i, title, description, event_date))
            
            for idx, (course_id, title, desc, date) in enumerate(events):
                f.write(f"({course_id}, '{title}', '{desc}', '{date.strftime('%Y-%m-%d %H:%M:%S')}', NOW())")
                if idx < len(events) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            print(f"  ✓ Generated {len(events)} calendar events")
            
            # ==================== FORUMS ====================
            print("\n[5/8] Generating forums...")
            f.write("-- FORUMS\n")
            f.write("INSERT INTO forums (course_id, title, description, created_at) VALUES\n")
            
            for idx, course_code in enumerate(courses, 1):
                title = f"Discussion Forum - {course_code}"
                description = f"Class discussion forum for {course_code}"
                f.write(f"({idx}, '{title}', '{description}', NOW())")
                if idx < len(courses):
                    f.write(",\n")
            f.write(";\n\n")
            print(f"  ✓ Generated {NUM_COURSES} forums")
            
            # ==================== DISCUSSION THREADS ====================
            print("\n[6/8] Generating discussion threads...")
            f.write("-- DISCUSSION THREADS\n")
            f.write("INSERT INTO discussion_threads (forum_id, title, content, author_id, created_at) VALUES\n")
            
            threads = []
            for course_idx, course_code in enumerate(courses[:50], 1):
                num_threads = random.randint(5, 15)
                forum_id = course_idx
                for j in range(num_threads):
                    title = f"Discussion Topic {j+1}: {random.choice(['Help needed', 'Question about', 'Interesting resource', 'Study group', 'Assignment help'])}"
                    content = f"This is the initial post for discussion topic {j+1}"
                    author_id = random.choice(student_ids[:1000])
                    threads.append((forum_id, title, content, author_id))
            
            for idx, (forum_id, title, content, author_id) in enumerate(threads):
                f.write(f"({forum_id}, '{title}', '{content}', '{author_id}', NOW())")
                if idx < len(threads) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            print(f"  ✓ Generated {len(threads)} discussion threads")
            
            # ==================== REPLIES ====================
            print("\n[7/8] Generating replies...")
            f.write("-- REPLIES\n")
            f.write("INSERT INTO discussion_replies (thread_id, content, author_id, parent_reply_id, created_at) VALUES\n")
            
            replies = []
            for i in range(3000):
                content = f"This is a reply to the discussion thread. Great points!"
                author_id = random.choice(student_ids[:5000])
                parent_reply_id = "NULL"
                replies.append((content, author_id, parent_reply_id))
            
            for idx, (content, author_id, parent_reply_id) in enumerate(replies):
                thread_id = random.randint(1, len(threads))
                f.write(f"({thread_id}, '{content}', '{author_id}', {parent_reply_id}, NOW())")
                if idx < len(replies) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            print(f"  ✓ Generated {len(replies)} replies")
            
            # ==================== COURSE SECTIONS ====================
            print("\n[8/8] Generating course sections and content...")
            f.write("-- COURSE SECTIONS\n")
            f.write("INSERT INTO course_sections (course_id, title, order_num, created_at) VALUES\n")
            
            sections = []
            for course_id in range(1, NUM_COURSES + 1):
                num_sections = random.randint(3, 8)
                section_titles = ['Introduction', 'Fundamentals', 'Core Concepts', 'Advanced Topics', 'Applications', 'Review', 'Projects', 'Final Exam']
                for j in range(num_sections):
                    title = section_titles[j % len(section_titles)] + f" {j+1}" if j > 0 else section_titles[j]
                    sections.append((course_id, title, j+1))
            
            for idx, (course_id, title, order_num) in enumerate(sections):
                f.write(f"({course_id}, '{title}', {order_num}, NOW())")
                if idx < len(sections) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            
            # Course Content
            f.write("-- COURSE CONTENT\n")
            f.write("INSERT INTO course_content (section_id, content_type, title, content_url, created_at) VALUES\n")
            
            content_types = ['link', 'file', 'slides', 'video', 'document']
            contents = []
            section_count = len(sections)
            for i in range(5000):
                content_type = random.choice(content_types)
                title = f"{random.choice(['Lecture Notes', 'Reading Material', 'Practice Problems', 'Quiz', 'Reference'])} {i+1}"
                content_url = f"/content/{random_string(15)}"
                contents.append((content_type, title, content_url))
            
            for idx, (content_type, title, content_url) in enumerate(contents):
                section_id = random.randint(1, section_count)
                f.write(f"({section_id}, '{content_type}', '{title}', '{content_url}', NOW())")
                if idx < len(contents) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            
            # Assignments
            f.write("-- ASSIGNMENTS\n")
            f.write("INSERT INTO assignments (course_id, title, description, due_date, max_score, created_at) VALUES\n")
            
            assignments = []
            for course_id in range(1, NUM_COURSES + 1):
                for i in range(random.randint(3, 5)):
                    due_date = random_date(start_date, end_date)
                    max_score = random.choice([100, 50, 20])
                    title = f"Assignment {i+1}"
                    description = f"Description for {title}"
                    assignments.append((course_id, title, description, due_date, max_score))
            
            for idx, (course_id, title, desc, due_date, max_score) in enumerate(assignments):
                f.write(f"({course_id}, '{title}', '{desc}', '{due_date.strftime('%Y-%m-%d %H:%M:%S')}', {max_score}, NOW())")
                if idx < len(assignments) - 1:
                    f.write(",\n")
            f.write(";\n\n")
            
            # Submissions
            f.write("-- SUBMISSIONS\n")
            f.write("INSERT INTO submissions (assignment_id, student_id, submission_text, submission_file, submitted_at, grade, graded_by, graded_at) VALUES\n")
            
            sample_size = min(20000, len(enrollments))
            submission_sample = random.sample(enrollments, sample_size)
            
            for idx, (student_id, course_code) in enumerate(submission_sample):
                course_id = course_ids[course_code]
                assignment_ids = [j+1 for j, (cid, _, _, _, _) in enumerate(assignments) if cid == course_id]
                if assignment_ids:
                    assignment_id = random.choice(assignment_ids)
                    submitted_at = random_date(start_date, end_date)
                    
                    if random.random() < 0.6:
                        grade = random.randint(60, 100)
                        graded_at = submitted_at + timedelta(days=random.randint(1, 14))
                        lecturer_id = random.choice(lecturer_ids)
                        f.write(f"({assignment_id}, '{student_id}', 'Submission content', '/submissions/{random_string()}.pdf', '{submitted_at.strftime('%Y-%m-%d %H:%M:%S')}', {grade}, '{lecturer_id}', '{graded_at.strftime('%Y-%m-%d %H:%M:%S')}')")
                    else:
                        f.write(f"({assignment_id}, '{student_id}', 'Submission content', '/submissions/{random_string()}.pdf', '{submitted_at.strftime('%Y-%m-%d %H:%M:%S')}', NULL, NULL, NULL)")
                    
                    if idx < len(submission_sample) - 1:
                        f.write(",\n")
            f.write(";\n\n")
            
            print(f"  ✓ Generated {len(sections)} course sections")
            print(f"  ✓ Generated {len(contents)} content items")
            print(f"  ✓ Generated {len(assignments)} assignments")
            print(f"  ✓ Generated {sample_size} submissions")
            
            # ==================== FINALIZE ====================
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
            f.flush()
            
            # Final summary
            print("\n" + "="*60)
            print("SQL FILE GENERATED SUCCESSFULLY!")
            print("="*60)
            print(f"  ✅ Admin: 1 (admin@uwi.edu)")
            print(f"  ✅ Lecturers: {NUM_LECTURERS:,} (*@uwi.edu)")
            print(f"  ✅ Students: {len(student_ids):,} (*@uwi.edu)")
            print(f"  ✅ Courses: {NUM_COURSES:,}")
            print(f"  ✅ Enrollments: {len(enrollments):,}")
            print(f"  ✅ Calendar Events: {len(events):,}")
            print(f"  ✅ Forums: {NUM_COURSES:,}")
            print(f"  ✅ Discussion Threads: {len(threads):,}")
            print(f"  ✅ Replies: {len(replies):,}")
            print(f"  ✅ Course Sections: {len(sections):,}")
            print(f"  ✅ Course Content: {len(contents):,}")
            print(f"  ✅ Assignments: {len(assignments):,}")
            print(f"  ✅ Submissions: {sample_size:,}")
            print("="*60)
            print("\n📁 File saved as: insert_data.sql")
            print("📧 All emails use @uwi.edu domain")
            
            # Verify count
            if len(student_ids) == NUM_STUDENTS:
                print(f"\n✅ VERIFIED: All {NUM_STUDENTS:,} students were generated!")
            else:
                print(f"\n⚠️ WARNING: Only {len(student_ids):,} out of {NUM_STUDENTS:,} students were generated!")
                
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    generate_sql_file()