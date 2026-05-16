import streamlit as st
from database import get_member_by_email, record_attendance, insert_member, get_all_sessions
from models import Member, BELT_ADULT
from datetime import date

st.set_page_config(page_title="Class Check-In", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f7f5; }
[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"] { display: none; }

p, h1, h2, h3, label, div, span, caption { color: #1a1a1a; }
button p { color: #ffffff !important; }

h1 { font-size: 1.6rem !important; font-weight: 600 !important; margin-bottom: 0.25rem !important; }
h2 { font-size: 1.1rem !important; font-weight: 500 !important; }

.session-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 1.5rem;
}
.session-name { font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; }
.session-detail { font-size: 0.85rem; color: #555 !important; }

.success-card {
    background: #f0faf4;
    border: 1px solid #b8e0c8;
    border-radius: 8px;
    padding: 24px 20px;
    text-align: center;
    margin-top: 1rem;
}
.success-tick { font-size: 2.5rem; margin-bottom: 0.5rem; }
.success-name { font-size: 1.3rem; font-weight: 600; color: #1a7a4a !important; margin-bottom: 0.25rem; }
.success-msg { font-size: 0.9rem; color: #555 !important; }

div[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
}

button[kind="primaryFormSubmit"], button[kind="secondaryFormSubmit"] {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

input, select { color: #1a1a1a !important; background: #fafafa !important; }
label { color: #333 !important; font-size: 0.9rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Read URL parameters ───────────────────────────────────────────────────────
params = st.query_params
session_id = params.get("session_id")
session_date = params.get("date")

if not session_id or not session_date:
    st.error("Invalid check-in link. Please scan the QR code again.")
    st.stop()

session_id = int(session_id)
sessions = get_all_sessions()
session = next((s for s in sessions if s.id == session_id), None)

if not session:
    st.error("Session not found. Please ask your coach for a new QR code.")
    st.stop()

display_date = date.fromisoformat(session_date)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# Check In")
st.markdown(f"""
<div class="session-card">
    <div class="session-name">{session.title}</div>
    <div class="session-detail">{session.day_of_week} {display_date.strftime('%d %b %Y')} &nbsp;·&nbsp; {session.start_time.strftime('%H:%M')}–{session.end_time.strftime('%H:%M')} &nbsp;·&nbsp; {session.gi_nogi}</div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "checkin_stage" not in st.session_state:
    st.session_state.checkin_stage = "email"
if "checkin_email" not in st.session_state:
    st.session_state.checkin_email = ""

# ── Stage 1: Email entry ──────────────────────────────────────────────────────
if st.session_state.checkin_stage == "email":
    st.markdown("## Enter your email")
    with st.form("email_form"):
        email = st.text_input("Email address", placeholder="your@email.com", label_visibility="collapsed")
        submitted = st.form_submit_button("Check In →", use_container_width=True)
        if submitted:
            if not email.strip():
                st.error("Please enter your email address.")
            else:
                member = get_member_by_email(email.strip().lower())
                if member:
                    record_attendance(member.id, session_id, session_date)
                    st.session_state.checkin_stage = "success"
                    st.session_state.checkin_name = member.first_name
                    st.rerun()
                else:
                    st.session_state.checkin_email = email.strip().lower()
                    st.session_state.checkin_stage = "register"
                    st.rerun()

# ── Stage 2: Quick registration ───────────────────────────────────────────────
elif st.session_state.checkin_stage == "register":
    st.markdown("## Create your account")
    st.caption("You're not in the system yet. Fill in your details to check in.")

    with st.form("register_form"):
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First name")
        with c2:
            last_name = st.text_input("Last name")

        date_of_birth = st.text_input("Date of birth (DD-MM-YYYY)")
        phone = st.text_input("Phone number")
        belt = st.selectbox("Belt", BELT_ADULT)
        stripes = st.selectbox("Stripes", [0, 1, 2, 3, 4])

        submitted = st.form_submit_button("Register and check in →", use_container_width=True)
        if submitted:
            try:
                new_member = Member(
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    belt=belt,
                    stripes=int(stripes),
                    phone=phone,
                    email=st.session_state.checkin_email
                )
                insert_member(new_member)
                created = get_member_by_email(st.session_state.checkin_email)
                if created:
                    record_attendance(created.id, session_id, session_date)
                st.session_state.checkin_stage = "success"
                st.session_state.checkin_name = first_name.strip().capitalize()
                st.rerun()
            except Exception as e:
                st.error(str(e))

# ── Stage 3: Success ──────────────────────────────────────────────────────────
elif st.session_state.checkin_stage == "success":
    st.markdown(f"""
<div class="success-card">
    <div class="success-tick">✓</div>
    <div class="success-name">Welcome, {st.session_state.checkin_name}!</div>
    <div class="success-msg">You're checked in to {session.title}.<br>You can close this page.</div>
</div>
""", unsafe_allow_html=True)