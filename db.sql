DROP TABLE IF EXISTS problems;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS contests;

CREATE TABLE tags(
	id varchar(100) PRIMARY KEY,
	name varchar(100) UNIQUE NOT NULL);

INSERT INTO tags VALUES
	('special', '*особая задача'),
	('NULL', 'NULL');

CREATE TABLE contests(
	id varchar(100) PRIMARY KEY,
	name varchar(100));

INSERT INTO contests VALUES
	('NULL', 'NULL');

CREATE TABLE problems(
	id varchar(100) NOT NULL, 
	tag_id varchar(100) REFERENCES tags(name) ON DELETE SET NULL,
	contest_id varchar(100) REFERENCES contests(id) ON DELETE SET NULL,
	name varchar(100) NOT NULL,
	difficulty smallint NOT NULL CHECK (difficulty > 0),
	passed_count integer NOT NULL CHECK (passed_count >= 0),
	url varchar(250) NOT NULL);
