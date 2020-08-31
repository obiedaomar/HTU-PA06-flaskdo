DROP TABLE IF EXISTS user;

-- Create 'User' table
CREATE TABLE User (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);