from .connection import get_connection

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

