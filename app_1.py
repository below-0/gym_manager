import streamlit as st
from models import Member, BELT_ADULT
from database import insert_member, get_all_members, delete_member, create_tables

# --- Page config ---
st.set_page_config(page_title="Academy Manager", layout="wide")

# --- Init DB ---
create_tables()

# --- Session state ---
if "view" not in st.session_state:
    st.session_state.view = None

# --- Title ---
st.title("Academy Manager")
st.divider()

# --- Navigation buttons ---
col1, col2, col3, col4 = st.columns([1, 1, 1, 5])

with col1:
    if st.button("View Members", use_container_width=True):
        if st.session_state.view == "members":
            st.session_state.view = None
        else:
            st.session_state.view = "members"

with col2:
    if st.button("Add Member", use_container_width=True):
        if st.session_state.view == "add":
            st.session_state.view = None
        else:
            st.session_state.view = "add"

with col3:
    if st.button("Delete Member", use_container_width=True):
        if st.session_state.view == "delete":
            st.session_state.view = None
        else:
            st.session_state.view = "delete"

st.divider()

# --- View Members ---
if st.session_state.view == "members":
    members = get_all_members()
    if not members:
        st.info("No members found.")
    else:
        st.subheader(f"Members ({len(members)})")
        for member in members:
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 3])
                c1.write(f"**#{member.id}**")
                c2.write(f"{member.first_name} {member.last_name}")
                c3.write(member.rank)
                c4.write(f"Age: {member.age}")
                c5.write(member.status)
        st.divider()
        if st.button("Hide Members"):
            st.session_state.view = None
            st.rerun()

# --- Add Member ---
elif st.session_state.view == "add":
    st.subheader("Add New Member")
    with st.form("add_member"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            date_of_birth = st.text_input("Date of Birth (DD-MM-YYYY)")
            belt = st.selectbox("Belt", BELT_ADULT)
            stripes = st.selectbox("Stripes", [0, 1, 2, 3, 4])
        with col2:
            phone = st.text_input("Phone Number")
            email = st.text_input("Email")


        submitted = st.form_submit_button("Add Member", use_container_width=True)
        if submitted:
            try:
                member = Member(
                    first_name, last_name,
                    date_of_birth, belt, int(stripes),
                    phone, email
                )
                insert_member(member)
                st.success(f"{member.first_name} {member.last_name} added successfully.")
            except ValueError as e:
                st.error(str(e))

# --- Delete Member ---
elif st.session_state.view == "delete":
    st.subheader("Delete Member")
    st.caption("View members first to find the member ID.")
    member_id = st.number_input("Enter Member ID", min_value=1, step=1)
    if st.button("Confirm Delete", type="primary"):
        delete_member(int(member_id))
        st.success(f"Member {int(member_id)} deleted.")