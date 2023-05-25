CREATE TABLE lecturers (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name TEXT
);

CREATE table courses (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    field_of_knowledge TEXT,
    short_name TEXT,
    full_name TEXT,
    size TEXT,
    description TEXT,
    direction TEXT,
    lecturer_id INT,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers (id),
    year INT
);

CREATE TABLE users (
	chat_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    email TEXT,
    direction TEXT
);

CREATE TABLE feedbacks (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES users (chat_id),
    date DATETIME,
    text TEXT
);

CREATE TABLE tags (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    type INT
);

CREATE TABLE course_context (
	course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    tag_id INT,
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE TABLE user_context (
	user_id INT,
    FOREIGN KEY (user_id) REFERENCES users (chat_id),
    tag_id INT,
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE TABLE metrics (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name TEXT
);

CREATE TABLE scores (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	metric_id INT,
    FOREIGN KEY (metric_id) REFERENCES metrics (id),
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES users (chat_id),
    date DATETIME,
    score INT
);

-- CREATE TABLE course_lecturer (
--     lecturer_id INT NOT NULL,
--     course_id INT NOT NULL,
--     PRIMARY KEY (lecturer_id, course_id),
--     CONSTRAINT member_lecturer_fk
--         FOREIGN KEY lecturer_fk (lecturer_id) REFERENCES lecturers (id)
--         ON DELETE CASCADE ON UPDATE CASCADE,
--     CONSTRAINT member_course_fk
--         FOREIGN KEY course_fk (course_id) REFERENCES courses (id)
--         ON DELETE CASCADE ON UPDATE CASCADE
-- )

-- DROP TABLE course_lecturer;
