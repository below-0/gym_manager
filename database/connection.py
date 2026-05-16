import sqlite3

def get_connection():
	conn = sqlite3.connect("academy.db")
	conn.execute("PRAGMA foreign_keys = ON")
	return conn

def create_tables():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS members(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		first_name text,
		last_name text,
		date_of_birth text,
		belt text,
		stripes integer,
		phone text,
		email text,
		status text
			)""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS sessions(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title text,
		day_of_week text, 
		start_time text,
		end_time text,
		gi_nogi text
		)""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS attendance(
		member_id INTEGER REFERENCES members(id),
		session_id INTEGER REFERENCES sessions(id),
		session_date text
		)""")
	conn.commit()
	conn.close()