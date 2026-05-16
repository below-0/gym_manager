from .connection import get_connection
from models import Session

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

def delete_session(id):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(" DELETE from sessions WHERE id = ?", (id, ))
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

