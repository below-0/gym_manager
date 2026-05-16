import streamlit as st
from models import Member, Session, BELT_ADULT
from database import (
    insert_member, get_all_members, delete_member,
    insert_session, get_all_sessions, delete_session, create_tables,
    record_attendance, get_member_attendance, get_session_attendance
)
from datetime import time, date

st.set_page_config(page_title="Academy Manager", layout="wide")

create_tables()

if "section" not in st.session_state:
    st.session_state.section = None
if "view" not in st.session_state:
    st.session_state.view = None

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
GI_NOGI = ["Gi", "No-Gi", "Mixed"]

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: transparent; }
.main-title {
    font-family: 'Georgia', serif;
    font-size: 2.2rem;
    font-weight: 400;
    letter-spacing: 0.08em;
    color: 1a1a1a;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.main-sub {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.divider { border: none; border-top: 0.5px solid #1e1e1e; margin: 1.5rem 0; }
.member-row {
    display: flex;
    align-items: center;
    padding: 12px 0;
    border-bottom: 0.5px solid #1e1e1e;
    gap: 16px;
}
.member-id { font-size: 11px; color: #444; min-width: 32px; }
.member-name { font-size: 14px; color: 1a1a1a; flex: 1; }
.member-rank { font-size: 12px; color: #c8b89a; flex: 1; }
.member-meta { font-size: 11px; color: #555; flex: 1; }
.timetable-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 8px;
    margin-top: 1rem;
}
.day-col { display: flex; flex-direction: column; gap: 6px; }
.day-header {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #555;
    text-transform: uppercase;
    padding-bottom: 8px;
    border-bottom: 0.5px solid #1e1e1e;
    margin-bottom: 4px;
}
.session-card {
    background: #f5f5f5;
    border: 0.5px solid #2a2a2a;
    border-radius: 3px;
    padding: 10px 12px;
}
.session-card.gi { border-left: 2px solid #c8b89a; }
.session-card.nogi { border-left: 2px solid #4a7c6e; }
.session-card.mixed { border-left: 2px solid #555; }
.session-title { font-size: 12px; color: 1a1a1a; margin-bottom: 4px; font-weight: 500; }
.session-time { font-size: 10px; color: #666; margin-bottom: 2px; }
.session-type { font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; }
.session-type.gi { color: #c8b89a; }
.session-type.nogi { color: #4a7c6e; }
.session-type.mixed { color: #888; }
.empty-day { font-size: 10px; color: #2a2a2a; font-style: italic; padding: 8px 0; }
.att-row {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 0.5px solid #ebebeb;
    gap: 16px;
    font-size: 13px;
    color: #1a1a1a;
}
.att-meta { font-size: 11px; color: #888; flex: 1; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Academy Manager</p>', unsafe_allow_html=True)
st.markdown('<p class="main-sub">Gym management system</p>', unsafe_allow_html=True)

col1, col2, col3, _ = st.columns([1, 1, 1, 5])
with col1:
    if st.button("Members", key="btn_members", use_container_width=True):
        if st.session_state.section == "members":
            st.session_state.section = None
            st.session_state.view = None
        else:
            st.session_state.section = "members"
            st.session_state.view = "view"
        st.rerun()
with col2:
    if st.button("Timetable", key="btn_timetable", use_container_width=True):
        if st.session_state.section == "timetable":
            st.session_state.section = None
            st.session_state.view = None
        else:
            st.session_state.section = "timetable"
            st.session_state.view = "view"
        st.rerun()
with col3:
    if st.button("Attendance", key="btn_attendance", use_container_width=True):
        if st.session_state.section == "attendance":
            st.session_state.section = None
            st.session_state.view = None
        else:
            st.session_state.section = "attendance"
            st.session_state.view = "record"
        st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── MEMBERS ──────────────────────────────────────────────────────────────────
if st.session_state.section == "members":
    nav1, nav2, nav3, _ = st.columns([1, 1, 1, 5])
    with nav1:
        if st.button("View", key="m_view", use_container_width=True):
            st.session_state.view = "view"; st.rerun()
    with nav2:
        if st.button("Add", key="m_add", use_container_width=True):
            st.session_state.view = "add"; st.rerun()
    with nav3:
        if st.button("Delete", key="m_delete", use_container_width=True):
            st.session_state.view = "delete"; st.rerun()

    if st.session_state.view == "view":
        members = get_all_members()
        if not members:
            st.markdown('<p style="color:#444; font-size:13px;">No members yet.</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="font-size:11px; color:#555; letter-spacing:0.1em; text-transform:uppercase;">{len(members)} members</p>', unsafe_allow_html=True)
            st.markdown('<div class="member-row"><span class="member-id">ID</span><span class="member-name">Name</span><span class="member-rank">Rank</span><span class="member-meta">Age</span><span class="member-meta">Status</span></div>', unsafe_allow_html=True)
            for m in members:
                st.markdown(f'''<div class="member-row">
                    <span class="member-id">{m.id}</span>
                    <span class="member-name">{m.first_name} {m.last_name}</span>
                    <span class="member-rank">{m.rank}</span>
                    <span class="member-meta">{m.age}</span>
                    <span class="member-meta">{m.status}</span>
                </div>''', unsafe_allow_html=True)

    elif st.session_state.view == "add":
        with st.form("add_member"):
            c1, c2 = st.columns(2)
            with c1:
                first_name = st.text_input("First name")
                date_of_birth = st.text_input("Date of birth (DD-MM-YYYY)")
                belt = st.selectbox("Belt", BELT_ADULT)
                phone = st.text_input("Phone")
            with c2:
                last_name = st.text_input("Last name")
                email = st.text_input("Email")
                stripes = st.selectbox("Stripes", [0, 1, 2, 3, 4])
            submitted = st.form_submit_button("Add Member", use_container_width=True)
            if submitted:
                try:
                    member = Member(
                        first_name=first_name, last_name=last_name,
                        date_of_birth=date_of_birth, belt=belt,
                        stripes=int(stripes), phone=phone, email=email
                    )
                    insert_member(member)
                    st.success(f"{member.first_name} {member.last_name} added.")
                except Exception as e:
                    st.error(str(e))

    elif st.session_state.view == "delete":
        st.markdown('<p style="font-size:12px; color:#555;">View members to find the ID first.</p>', unsafe_allow_html=True)
        member_id = st.number_input("Member ID", min_value=1, step=1)
        if st.button("Confirm delete", type="primary"):
            delete_member(int(member_id))
            st.success(f"Member {int(member_id)} deleted.")

# ── TIMETABLE ────────────────────────────────────────────────────────────────
elif st.session_state.section == "timetable":
    nav1, nav2, nav3, _ = st.columns([1, 1, 1, 5])
    with nav1:
        if st.button("View", key="t_view", use_container_width=True):
            st.session_state.view = "view"; st.rerun()
    with nav2:
        if st.button("Add", key="t_add", use_container_width=True):
            st.session_state.view = "add"; st.rerun()
    with nav3:
        if st.button("Delete", key="t_delete", use_container_width=True):
            st.session_state.view = "delete"; st.rerun()

    if st.session_state.view == "view":
        sessions = get_all_sessions()
        sessions_by_day = {day: [] for day in DAYS}
        for s in sessions:
            if s.day_of_week in sessions_by_day:
                sessions_by_day[s.day_of_week].append(s)
        for day in DAYS:
            sessions_by_day[day].sort(key=lambda s: s.start_time)

        grid_html = '<div class="timetable-grid">'
        for day in DAYS:
            grid_html += f'<div class="day-col"><div class="day-header">{day[:3]}</div>'
            day_sessions = sessions_by_day[day]
            if not day_sessions:
                grid_html += '<div class="empty-day">—</div>'
            else:
                for s in day_sessions:
                    gi_class = "gi" if s.gi_nogi == "Gi" else ("nogi" if s.gi_nogi == "No-Gi" else "mixed")
                    grid_html += f'''<div class="session-card {gi_class}">
                        <div class="session-title">{s.title}</div>
                        <div class="session-time">{s.start_time.strftime("%H:%M")} – {s.end_time.strftime("%H:%M")}</div>
                        <div class="session-type {gi_class}">{s.gi_nogi}</div>
                    </div>'''
            grid_html += '</div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

    elif st.session_state.view == "add":
        with st.form("add_session"):
            title = st.text_input("Session title")
            c1, c2, c3 = st.columns(3)
            with c1:
                day = st.selectbox("Day", DAYS)
            with c2:
                start_time = st.time_input("Start time", value=time(9, 0))
            with c3:
                end_time = st.time_input("End time", value=time(10, 0))
            gi_nogi = st.selectbox("Gi / No-Gi", GI_NOGI)
            submitted = st.form_submit_button("Add Session", use_container_width=True)
            if submitted:
                try:
                    session = Session(
                        title=title, day_of_week=day,
                        start_time=start_time, end_time=end_time,
                        gi_nogi=gi_nogi
                    )
                    insert_session(session)
                    st.success(f"{session.title} added to {day}.")
                except Exception as e:
                    st.error(str(e))

    elif st.session_state.view == "delete":
        st.markdown('<p style="font-size:12px; color:#555;">View timetable to find the session ID.</p>', unsafe_allow_html=True)
        session_id = st.number_input("Session ID", min_value=1, step=1)
        if st.button("Confirm delete", type="primary"):
            delete_session(int(session_id))
            st.success(f"Session {int(session_id)} deleted.")

# ── ATTENDANCE ───────────────────────────────────────────────────────────────
elif st.session_state.section == "attendance":
    nav1, nav2, nav3, _ = st.columns([1, 1, 1, 5])
    with nav1:
        if st.button("Record", key="a_record", use_container_width=True):
            st.session_state.view = "record"; st.rerun()
    with nav2:
        if st.button("By Session", key="a_session", use_container_width=True):
            st.session_state.view = "by_session"; st.rerun()
    with nav3:
        if st.button("By Member", key="a_member", use_container_width=True):
            st.session_state.view = "by_member"; st.rerun()

    # ── Record attendance ──
    if st.session_state.view == "record":
        members = get_all_members()
        sessions = get_all_sessions()

        if not members or not sessions:
            st.markdown('<p style="color:#888; font-size:13px;">Add members and sessions before recording attendance.</p>', unsafe_allow_html=True)
        else:
            with st.form("record_attendance"):
                member_options = {f"{m.first_name} {m.last_name} (ID {m.id})": m.id for m in members}
                session_options = {f"{s.title} — {s.day_of_week} {s.start_time.strftime('%H:%M')} (ID {s.id})": s.id for s in sessions}

                selected_member = st.selectbox("Member", list(member_options.keys()))
                selected_session = st.selectbox("Session", list(session_options.keys()))
                session_date = st.date_input("Date", value=date.today())

                submitted = st.form_submit_button("Record Attendance", use_container_width=True)
                if submitted:
                    try:
                        record_attendance(
                            member_options[selected_member],
                            session_options[selected_session],
                            session_date.strftime("%Y-%m-%d")
                        )
                        st.success("Attendance recorded.")
                    except Exception as e:
                        st.error(str(e))

    # ── View by session ──
    elif st.session_state.view == "by_session":
        sessions = get_all_sessions()
        members = get_all_members()
        member_lookup = {m.id: f"{m.first_name} {m.last_name}" for m in members}

        if not sessions:
            st.markdown('<p style="color:#888; font-size:13px;">No sessions yet.</p>', unsafe_allow_html=True)
        else:
            session_options = {f"{s.title} — {s.day_of_week} {s.start_time.strftime('%H:%M')} (ID {s.id})": s.id for s in sessions}
            selected_session = st.selectbox("Session", list(session_options.keys()))

            c1, c2 = st.columns(2)
            with c1:
                date_from = st.date_input("From", value=date(date.today().year, date.today().month, 1))
            with c2:
                date_to = st.date_input("To", value=date.today())

            if st.button("Search", use_container_width=False):
                session_id = session_options[selected_session]
                records = get_session_attendance(session_id)
                filtered = [
                    r for r in records
                    if date_from.strftime("%Y-%m-%d") <= r["session_date"] <= date_to.strftime("%Y-%m-%d")
                ]
                if not filtered:
                    st.markdown('<p style="color:#888; font-size:13px;">No attendance records in this range.</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="font-size:11px; color:#555; text-transform:uppercase; letter-spacing:0.1em;">{len(filtered)} records</p>', unsafe_allow_html=True)
                    for r in filtered:
                        name = member_lookup.get(r["member_id"], f"Member {r['member_id']}")
                        st.markdown(f'<div class="att-row"><span style="flex:1">{name}</span><span class="att-meta">{r["session_date"]}</span></div>', unsafe_allow_html=True)

    # ── View by member ──
    elif st.session_state.view == "by_member":
        members = get_all_members()
        sessions = get_all_sessions()
        session_lookup = {s.id: f"{s.title} — {s.day_of_week} {s.start_time.strftime('%H:%M')}" for s in sessions}

        if not members:
            st.markdown('<p style="color:#888; font-size:13px;">No members yet.</p>', unsafe_allow_html=True)
        else:
            member_options = {f"{m.first_name} {m.last_name} (ID {m.id})": m.id for m in members}
            selected_member = st.selectbox("Member", list(member_options.keys()))

            c1, c2 = st.columns(2)
            with c1:
                date_from = st.date_input("From", value=date(date.today().year, date.today().month, 1), key="mf")
            with c2:
                date_to = st.date_input("To", value=date.today(), key="mt")

            if st.button("Search", key="search_member", use_container_width=False):
                member_id = member_options[selected_member]
                records = get_member_attendance(member_id)
                filtered = [
                    r for r in records
                    if date_from.strftime("%Y-%m-%d") <= r["session_date"] <= date_to.strftime("%Y-%m-%d")
                ]
                if not filtered:
                    st.markdown('<p style="color:#888; font-size:13px;">No attendance records in this range.</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="font-size:11px; color:#555; text-transform:uppercase; letter-spacing:0.1em;">{len(filtered)} classes attended</p>', unsafe_allow_html=True)
                    for r in filtered:
                        session_name = session_lookup.get(r["session_id"], f"Session {r['session_id']}")
                        st.markdown(f'<div class="att-row"><span style="flex:1">{session_name}</span><span class="att-meta">{r["session_date"]}</span></div>', unsafe_allow_html=True)