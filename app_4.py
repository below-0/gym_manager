import streamlit as st
from models import Member, Session, BELT_ADULT
from database import (
    insert_member, get_all_members, delete_member,
    insert_session, get_all_sessions, delete_session, create_tables,
    record_attendance, get_member_attendance, get_session_attendance
)
from datetime import time, date, timedelta

st.set_page_config(page_title="Academy Manager", layout="wide")

create_tables()

# ── Session state defaults ────────────────────────────────────────────────────
for key, default in {
    "section": None,
    "view": None,
    "selected_member_id": None,
    "selected_session_id": None,
    "selected_session_date": None,
    "week_offset": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
GI_NOGI = ["Gi", "No-Gi", "Mixed"]

# ── Minimal style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: transparent; }
.divider { border: none; border-top: 0.5px solid #e0e0e0; margin: 1.5rem 0; }
.member-row {
    display: flex; align-items: center;
    padding: 12px 0; border-bottom: 0.5px solid #e0e0e0;
    gap: 16px; font-size: 13px; color: #1a1a1a;
}
.member-id { font-size: 11px; color: #888; min-width: 32px; }
.member-rank { font-size: 12px; color: #b09060; }
.att-row {
    display: flex; align-items: center;
    padding: 10px 0; border-bottom: 0.5px solid #ebebeb;
    gap: 16px; font-size: 13px; color: #1a1a1a;
}
.att-meta { font-size: 11px; color: #888; }
</style>
""", unsafe_allow_html=True)

st.title("Academy Manager")

# ── Top navigation ────────────────────────────────────────────────────────────
col1, col2, col3, _ = st.columns([1, 1, 1, 5])

def nav_click(section):
    if st.session_state.section == section:
        st.session_state.section = None
        st.session_state.view = None
    else:
        st.session_state.section = section
        st.session_state.view = "view" if section != "attendance" else "by_session"
    st.session_state.selected_member_id = None
    st.session_state.selected_session_id = None
    st.session_state.selected_session_date = None

with col1:
    if st.button("Members", use_container_width=True):
        nav_click("members"); st.rerun()
with col2:
    if st.button("Timetable", use_container_width=True):
        nav_click("timetable"); st.rerun()
with col3:
    if st.button("Attendance", use_container_width=True):
        nav_click("attendance"); st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── MEMBERS ───────────────────────────────────────────────────────────────────
if st.session_state.section == "members":
    n1, n2, n3, _ = st.columns([1, 1, 1, 5])
    with n1:
        if st.button("View", key="m_view", use_container_width=True):
            st.session_state.view = "view"; st.rerun()
    with n2:
        if st.button("Add", key="m_add", use_container_width=True):
            st.session_state.view = "add"; st.rerun()
    with n3:
        if st.button("Delete", key="m_delete", use_container_width=True):
            st.session_state.view = "delete"; st.rerun()

    if st.session_state.view == "view":
        members = get_all_members()
        if not members:
            st.info("No members yet.")
        else:
            st.caption(f"{len(members)} members")
            st.markdown('<div class="member-row"><span class="member-id">ID</span><span style="flex:1">Name</span><span style="flex:1" class="member-rank">Rank</span><span style="flex:1">Age</span><span style="flex:1">Status</span></div>', unsafe_allow_html=True)
            for m in members:
                st.markdown(f'<div class="member-row"><span class="member-id">{m.id}</span><span style="flex:1">{m.first_name} {m.last_name}</span><span style="flex:1" class="member-rank">{m.rank}</span><span style="flex:1">{m.age}</span><span style="flex:1">{m.status}</span></div>', unsafe_allow_html=True)

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
            if st.form_submit_button("Add Member", use_container_width=True):
                try:
                    member = Member(first_name=first_name, last_name=last_name,
                        date_of_birth=date_of_birth, belt=belt,
                        stripes=int(stripes), phone=phone, email=email)
                    insert_member(member)
                    st.success(f"{member.first_name} {member.last_name} added.")
                except Exception as e:
                    st.error(str(e))

    elif st.session_state.view == "delete":
        st.caption("View members to find the ID first.")
        member_id = st.number_input("Member ID", min_value=1, step=1)
        if st.button("Confirm delete", type="primary"):
            delete_member(int(member_id))
            st.success(f"Member {int(member_id)} deleted.")

# ── TIMETABLE ─────────────────────────────────────────────────────────────────
elif st.session_state.section == "timetable":
    n1, n2, n3, _ = st.columns([1, 1, 1, 5])
    with n1:
        if st.button("View", key="t_view", use_container_width=True):
            st.session_state.view = "view"; st.rerun()
    with n2:
        if st.button("Add", key="t_add", use_container_width=True):
            st.session_state.view = "add"; st.rerun()
    with n3:
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

        cols = st.columns(7)
        for i, day in enumerate(DAYS):
            with cols[i]:
                st.markdown(f"**{day[:3]}**")
                for s in sessions_by_day[day]:
                    gi = "Gi" if s.gi_nogi == "Gi" else ("NG" if s.gi_nogi == "No-Gi" else "Mix")
                    st.caption(f"{s.start_time.strftime('%H:%M')}–{s.end_time.strftime('%H:%M')} · {gi}")
                    st.write(s.title)
                if not sessions_by_day[day]:
                    st.caption("—")

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
            if st.form_submit_button("Add Session", use_container_width=True):
                try:
                    session = Session(title=title, day_of_week=day,
                        start_time=start_time, end_time=end_time, gi_nogi=gi_nogi)
                    insert_session(session)
                    st.success(f"{session.title} added to {day}.")
                except Exception as e:
                    st.error(str(e))

    elif st.session_state.view == "delete":
        st.caption("View timetable to find the session ID.")
        session_id = st.number_input("Session ID", min_value=1, step=1)
        if st.button("Confirm delete", type="primary"):
            delete_session(int(session_id))
            st.success(f"Session {int(session_id)} deleted.")

# ── ATTENDANCE ────────────────────────────────────────────────────────────────
elif st.session_state.section == "attendance":
    n1, n2, n3, _ = st.columns([1, 1, 1, 5])
    with n1:
        if st.button("Record", key="a_record", use_container_width=True):
            st.session_state.view = "record"
            st.session_state.selected_session_id = None
            st.session_state.selected_session_date = None
            st.rerun()
    with n2:
        if st.button("By Session", key="a_session", use_container_width=True):
            st.session_state.view = "by_session"
            st.session_state.selected_session_id = None
            st.session_state.selected_session_date = None
            st.rerun()
    with n3:
        if st.button("By Member", key="a_member", use_container_width=True):
            st.session_state.view = "by_member"
            st.session_state.selected_member_id = None
            st.rerun()

    # ── Record ────────────────────────────────────────────────────────────────
    if st.session_state.view == "record":
        members = get_all_members()
        sessions = get_all_sessions()
        if not members or not sessions:
            st.info("Add members and sessions before recording attendance.")
        else:
            with st.form("record_attendance"):
                member_options = {f"{m.first_name} {m.last_name} (ID {m.id})": m.id for m in members}
                session_options = {f"{s.title} — {s.day_of_week} {s.start_time.strftime('%H:%M')}": s.id for s in sessions}
                selected_member = st.selectbox("Member", list(member_options.keys()))
                selected_session = st.selectbox("Session", list(session_options.keys()))
                session_date = st.date_input("Date", value=date.today())
                if st.form_submit_button("Record Attendance", use_container_width=True):
                    try:
                        record_attendance(
                            member_options[selected_member],
                            session_options[selected_session],
                            session_date.strftime("%Y-%m-%d")
                        )
                        st.success("Attendance recorded.")
                    except Exception as e:
                        st.error(str(e))

    # ── By session — clickable calendar ───────────────────────────────────────
    elif st.session_state.view == "by_session":
        sessions = get_all_sessions()
        members = get_all_members()
        member_lookup = {m.id: f"{m.first_name} {m.last_name}" for m in members}

        today = date.today()
        week_start = today - timedelta(days=today.weekday()) + timedelta(weeks=st.session_state.week_offset)
        week_end = week_start + timedelta(days=6)

        wc1, wc2, wc3, _ = st.columns([1, 1, 2, 4])
        with wc1:
            if st.button("← Prev week", use_container_width=True):
                st.session_state.week_offset -= 1
                st.session_state.selected_session_id = None
                st.session_state.selected_session_date = None
                st.rerun()
        with wc2:
            if st.button("This week", use_container_width=True):
                st.session_state.week_offset = 0
                st.session_state.selected_session_id = None
                st.session_state.selected_session_date = None
                st.rerun()
        with wc3:
            st.caption(f"{week_start.strftime('%d %b')} – {week_end.strftime('%d %b %Y')}")

        sessions_by_day = {day: [] for day in DAYS}
        for s in sessions:
            if s.day_of_week in sessions_by_day:
                sessions_by_day[s.day_of_week].append(s)
        for day in DAYS:
            sessions_by_day[day].sort(key=lambda s: s.start_time)

        day_dates = {DAYS[i]: week_start + timedelta(days=i) for i in range(7)}

        cal_cols = st.columns(7)
        for i, day in enumerate(DAYS):
            day_date = day_dates[day]
            is_future = day_date > today
            with cal_cols[i]:
                if day_date == today:
                    st.markdown(f"**{day[:3]} {day_date.strftime('%d')}** ◆")
                else:
                    st.markdown(f"**{day[:3]} {day_date.strftime('%d')}**")

                day_sessions = sessions_by_day[day]
                if not day_sessions:
                    st.caption("—")
                for s in day_sessions:
                    gi = "Gi" if s.gi_nogi == "Gi" else ("NG" if s.gi_nogi == "No-Gi" else "Mix")
                    label = f"{s.start_time.strftime('%H:%M')} {s.title}\n{gi}"
                    if is_future:
                        st.button(label, key=f"cal_{s.id}_{day_date}", disabled=True, use_container_width=True)
                    else:
                        if st.button(label, key=f"cal_{s.id}_{day_date}", use_container_width=True):
                            st.session_state.selected_session_id = s.id
                            st.session_state.selected_session_date = day_date.strftime("%Y-%m-%d")
                            st.rerun()

        # Show attendance for selected session
        if st.session_state.selected_session_id and st.session_state.selected_session_date:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            selected_session = next((s for s in sessions if s.id == st.session_state.selected_session_id), None)
            display_date = date.fromisoformat(st.session_state.selected_session_date)

            if selected_session:
                st.markdown(f"**{selected_session.title}** — {display_date.strftime('%A %d %b %Y')}")
                records = get_session_attendance(st.session_state.selected_session_id)
                filtered = [r for r in records if r["session_date"] == st.session_state.selected_session_date]

                if not filtered:
                    st.caption("No attendance recorded for this session.")
                else:
                    st.caption(f"{len(filtered)} attended")
                    for r in filtered:
                        name = member_lookup.get(r["member_id"], f"Member {r['member_id']}")
                        st.markdown(f'<div class="att-row"><span>{name}</span></div>', unsafe_allow_html=True)

    # ── By member — card grid ─────────────────────────────────────────────────
    elif st.session_state.view == "by_member":
        members = get_all_members()
        sessions = get_all_sessions()
        session_lookup = {s.id: f"{s.title} — {s.day_of_week} {s.start_time.strftime('%H:%M')}" for s in sessions}

        if not members:
            st.info("No members yet.")
        else:
            if st.session_state.selected_member_id is None:
                st.caption("Select a member to view their attendance.")
                cols = st.columns(4)
                for i, m in enumerate(members):
                    with cols[i % 4]:
                        if st.button(f"{m.first_name} {m.last_name}\n{m.rank}", key=f"mc_{m.id}", use_container_width=True):
                            st.session_state.selected_member_id = m.id
                            st.rerun()
            else:
                selected = next((m for m in members if m.id == st.session_state.selected_member_id), None)
                if selected:
                    bc, _ = st.columns([1, 6])
                    with bc:
                        if st.button("← All members", use_container_width=True):
                            st.session_state.selected_member_id = None
                            st.rerun()

                    st.subheader(f"{selected.first_name} {selected.last_name}")
                    st.caption(selected.rank)

                    fc1, fc2 = st.columns(2)
                    with fc1:
                        date_from = st.date_input("From", value=date(date.today().year, 1, 1))
                    with fc2:
                        date_to = st.date_input("To", value=date.today())

                    records = get_member_attendance(st.session_state.selected_member_id)
                    filtered = [
                        r for r in records
                        if date_from.strftime("%Y-%m-%d") <= r["session_date"] <= date_to.strftime("%Y-%m-%d")
                    ]

                    st.caption(f"{len(filtered)} classes attended")

                    if not filtered:
                        st.info("No attendance in this period.")
                    else:
                        for r in sorted(filtered, key=lambda x: x["session_date"], reverse=True):
                            session_name = session_lookup.get(r["session_id"], f"Session {r['session_id']}")
                            st.markdown(f'<div class="att-row"><span style="flex:2">{session_name}</span><span class="att-meta">{r["session_date"]}</span></div>', unsafe_allow_html=True)