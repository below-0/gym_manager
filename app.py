import streamlit as st
from models import Member, BELT_ADULT, BELT_CHILD
from database import insert_member, get_all_members, delete_member, create_table


create_table()

st.title("Academy Manager")

st.button("View Members")
members = get_all_members()
for member in members:
    st.write(member)


with st.form("add_member"): 
	first_name = st.text_input("First name: ")
	last_name = st.text_input("Last name: ")
	date_of_birth = st.text_input("Date of Birth (DD-MM-YYYY): ")
	belt = st.selectbox("Belt: ", BELT_ADULT)
	stripes = st.selectbox("Stripes: ", ['0', '1', '2', '3', '4'])
	phone = st.text_input("Phone number: ")
	email = st.text_input("Email: ")
	submitted = st.form_submit_button("Add Member")
	if submitted:
		member = Member(first_name, last_name,
			date_of_birth, belt, int(stripes),
			phone, email)
		insert_member(member)

with st.form('delete_member'):
	member_id = st.number_input("Member ID", min_value=1, step=1)
	submitted = st.form_submit_button("Delete Member")
	if submitted:
		delete_member(int(member_id))
		st.success("Member deleted")
