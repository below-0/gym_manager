from .connection import get_connection
from models import Member
from datetime import datetime

def insert_member(member):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("""
	 INSERT INTO members (first_name, last_name, date_of_birth,
	 	belt, stripes, phone, email, status) 
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (member.first_name, member.last_name, 
	 	member.date_of_birth.strftime("%d-%m-%Y"), member.belt, member.stripes,
	 	member.phone, member.email.lower(), member.status ))
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

def get_member_by_email(email):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM members WHERE email = ?", (email, ))
	row = cursor.fetchone()
	if row is None:
		return None
	member = Member (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], id=row[0])
	conn.close()
	return member