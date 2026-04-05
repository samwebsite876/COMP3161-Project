

USE coursemanagement;

-- Calendar Events Table
CREATE TABLE calendar_events (
    event_id INT NOT NULL AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATE,
    created_by VARCHAR(20) NOT NULL,
    PRIMARY KEY (event_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Forums Table
CREATE TABLE forums (
    forum_id INT NOT NULL AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_by VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (forum_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Threads Table
CREATE TABLE threads (
    thread_id INT NOT NULL AUTO_INCREMENT,
    forum_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_by VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (thread_id),
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Posts Table (for discussion and replies)
CREATE TABLE posts (
    post_id INT NOT NULL AUTO_INCREMENT,
    thread_id INT NOT NULL,
    user_id VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    parent_post_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id),
    FOREIGN KEY (thread_id) REFERENCES threads(thread_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_post_id) REFERENCES posts(post_id)
);