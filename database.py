import sqlite3
from models import Member

connection = sqlite3.connect("members.db")

cursor = connection.cursor()

def create_table():
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
	connection.commit()

create_table()

def insert_member(member):
	cursor.execute("""
	 INSERT INTO members (first_name, last_name, date_of_birth,
	 	belt, stripes,phone, email, status) 
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (member.first_name, member.last_name, 
	 	member.date_of_birth.strftime("%d-%m-%Y"), member.belt, member.stripes,
	 	member.phone, member.email, member.status ))
	connection.commit()

def delete_member(id):
	cursor.execute(" DELETE from members WHERE id = ?", (id, ))
	connection.commit()

def get_all_members():
	cursor.execute("SELECT * FROM members")
	rows = cursor.fetchall()
	members =[]
	for row in rows:
		member = Member (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
		members.append(member) 
	return members


if __name__ == "__main__":
	"""
	m = Member(
		"darren", "cairns ",
		"24-05-1989", "Black Belt",
		0, "07454052135",
		"test@email.com"
		)
	insert_member(m)
	
	"""
	delete_member(14)
	members = get_all_members()
	for member in members:
		print(member)

