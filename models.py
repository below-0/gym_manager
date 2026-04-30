from datetime import date, datetime

STATUS = ["Active", "Paused", "Cancelled"]
BELT_ADULT = ["White Belt", "Blue Belt", "Purple Belt", "Brown Belt", "Black Belt"]
BELT_CHILD = [
"White Belt", 
"Grey + White Belt", "Grey Belt", "Grey + Black Belt",
"Orange + White Belt", "Orange Belt", "Orange + Black Belt",
"Yellow + White Belt", "Yellow Belt", "Yellow + Black Belt",
"Green + White Belt", "Green Belt", "Green + Black Belt"
]

class Member:
	def __init__(
		self, first_name, last_name,
		date_of_birth, belt, stripes,
		phone, email, status = "Active"
		):
		self.first_name = first_name
		self.last_name =last_name
		try:
			self.date_of_birth = datetime.strptime(date_of_birth, "%d-%m-%Y").date()
		except ValueError:
			raise ValueError ("Date of birth must be in the format DD-MM-YYYY")
		self.belt = belt
		self.stripes = stripes
		self.phone = phone
		self.email = email
		self._date_joined = date.today()
		self.status = status

	def __str__(self):
		return (
			f"{self.first_name} {self.last_name} | "
			f"{self.rank} | {self.age} | {self.phone} | "
			f"{self.email} | Joined: {self.date_joined.strftime("%d-%b-%Y")} | "
			f"Membership Status: {self.status}"
		)

	def _sanitise_name(self, value):
		return value.strip().capitalize()

	@property
	def first_name(self):
		return self._first_name
	
	@first_name.setter
	def first_name(self, value):
		self._first_name = self._sanitise_name(value)

	@property
	def last_name(self):
		return self._last_name

	@last_name.setter
	def last_name(self, value):
		self._last_name = self._sanitise_name(value)

	@property
	def age(self):
		today = date.today()
		age = today.year - self.date_of_birth.year
		if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
			age -= 1
		return age

	@property
	def member_type(self):
		if self.age >= 16:
			return "Adult"
		else:
			return "Child"

	@property
	def belt(self):
		return self._belt

	@belt.setter
	def belt(self, value):
		if self.member_type == "Adult":
			valid_belts = BELT_ADULT
		else:
			valid_belts = BELT_CHILD
		if value not in valid_belts:
			raise ValueError (f" {value} is not a valid belt")
		self._belt = value

	@property
	def stripes(self):
		return self._stripes

	@stripes.setter
	def stripes(self, value):
		if not 0 <= value <= 4:
			raise ValueError ("stripes must be a number between 0 and 4")
		self._stripes = value
	
	@property
	def rank(self):
		if self.stripes == 0:
			return self.belt
		elif self.stripes == 1:
			return f"{self.belt} - {self.stripes} stripe"
		else:
			return f"{self.belt} - {self.stripes} stripes"

	@property
	def phone(self):
		return self._phone

	@phone.setter
	def phone(self, value):
		if not 8 <= len(value) <= 15:
			raise ValueError ("Please enter a valid phone number")
		self._phone = value


	@property
	def date_joined(self):
		return self._date_joined


	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, value):
		if value not in STATUS:
			raise ValueError("not a valid membership status")
		self._status = value
	


	

	







if __name__ == "__main__":
	m = Member(
		"andrew", "cairns ",
		"24-05-1986", "Black Belt",
		0, "07454052135",
		"test@email.com"
		)
	print(m)


	
