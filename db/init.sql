create database students;
use students;

CREATE TABLE test_table (
  name VARCHAR(20),
  location VARCHAR(30)
);

INSERT INTO test_table
  (name, location)
VALUES
  ('Nawfel', '48.866667,2.333333'),
  ('Alex', '40.730610,-73.935242');