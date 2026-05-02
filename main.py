from models import Member
from database import insert_member, get_all_members, delete_member

def create_member():
	first_name = input("First name: ")
	last_name = input("Last name: ")
	date_of_birth = input("Date of Birth (DD-MM-YYYY): ")
	belt = input("Belt: ")
	stripes = int(input("Stripes: "))
	phone = input("Phone number: ")
	email = input("Email: ")
	member = Member(first_name, last_name,
		date_of_birth, belt, stripes,
		phone, email)
	insert_member(member)


def main():
	while True:
		print("Welcome to Academy Manager")
		print("What would you like to do?")
		print("1. Add a new member")
		print("2. View members")
		print("3. Delete a member")
		print("4. Quit")

		choice = input (">").strip()

		if choice == "1":
			create_member()
		elif choice == "2":
			members = get_all_members()
			for member in members:
				print (member)
		elif choice == "3":
			member_id = int(input("Enter member ID to delete: "))
			delete_member(member_id)
		elif choice == "4":
			break
		else:
			print("invalid choice")

main()