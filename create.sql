-- create.sql
-- ToDoList App SQLITE3 Create Table SQL

DROP TABLE IF EXISTS Tasks;
CREATE TABLE Tasks (
	task_id INTEGER PRIMARY KEY,
	created REAL,
	status INT DEFAULT 0,
	name TEXT
);

DROP TABLE IF EXISTS Tags;
CREATE TABLE Tags (
	tag_id INT PRIMARY KEY,
	created REAL,
	name TEXT
);

-- Tasks and Tags are a many-to-many relationship
--+  so we require an intermediate table to represent this.
DROP TABLE IF EXISTS Tags_to_Tasks;
CREATE TABLE Tags_to_Tasks (
	task_id INT,
	tag_id INT,
	FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
	FOREIGN KEY (tag_id) REFERENCES Tags(tag_id),
	PRIMARY KEY (task_id, tag_id)
);