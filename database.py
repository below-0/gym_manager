import sqlite3
from models import Member, Session
from datetime import datetime

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

def insert_member(member):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
	 INSERT INTO members (first_name, last_name, date_of_birth,
	 	belt, stripes, phone, email, status) 
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (member.first_name, member.last_name, 
	 	member.date_of_birth.strftime("%d-%m-%Y"), member.belt, member.stripes,
	 	member.phone, member.email, member.status ))
	conn.commit()
	conn.close()

def delete_member(id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(" DELETE from members WHERE id = ?", (id, ))
	conn.commit()
	conn.close()

def get_all_members():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM members")
	rows = cursor.fetchall()
	conn.close()
	members =[]
	for row in rows:
		member = Member (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], id=row[0])
		members.append(member) 
	return members

def insert_session(session):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		INSERT INTO sessions (title, day_of_week,
			start_time, end_time, gi_nogi)
		VALUES(?, ?, ?, ?, ?)""", (session.title, session.day_of_week,
			session.start_time.strftime("%H:%M"), 
			session.end_time.strftime("%H:%M"), session.gi_nogi))
	conn.commit()
	conn.close()

def get_all_sessions():
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM sessions")
	rows = cursor.fetchall()
	conn.close()
	sessions =[]
	for row in rows:
		session = Session (title=row[1], day_of_week=row[2], start_time=row[3], 
		end_time=row[4], gi_nogi=row[5], id=row[0])
		sessions.append(session) 
	return sessions

def delete_session(id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(" DELETE from sessions WHERE id = ?", (id, ))
	conn.commit()
	conn.close()

def record_attendance(member_id, session_id, session_date):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
		INSERT INTO attendance (member_id, session_id, session_date)
		VALUES (?, ?, ?)""", (member_id, session_id, session_date))
	conn.commit()
	conn.close()

def get_member_attendance(member_id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM attendance WHERE member_id = ?", (member_id,))
	rows = cursor.fetchall()
	conn.close()
	member_attendance =[]
	for row in rows:
		member_attendance.append({
			"member_id": row[0],
			"session_id": row[1],
			"session_date": row[2]
			})
	return member_attendance

def get_session_attendance(session_id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM attendance WHERE session_id = ?", (session_id,))
	rows = cursor.fetchall()
	conn.close()
	session_attendance =[]
	for row in rows:
		session_attendance.append({
			"member_id": row[0],
			"session_id": row[1],
			"session_date": row[2]
			})
	return session_attendance


if __name__ == "__main__":
    record_attendance(17, 3, "2026-05-12")
    print(get_member_attendance(17))
    print(get_session_attendance(3))
