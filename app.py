import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Alpha vs Omega Tracker", layout="wide")

# ---------- Helpers ----------
def init_state(n_subteams: int):
    st.session_state['teams'] = {
        'Alpha': [
            {
                'name': f'Alpha-{i+1}',
                'roles': ['Killing Team', 'Revive Team', 'Tasks Team'],
                'dead_until': 0.0
            }
            for i in range(n_subteams)
        ],
        'Omega': [
            {
                'name': f'Omega-{i+1}',
                'roles': ['Killing Team', 'Revive Team', 'Tasks Team'],
                'dead_until': 0.0
            }
            for i in range(n_subteams)
        ]
    }


def format_seconds(s: int) -> str:
    m = s // 60
    sec = s % 60
    return f"{m:02d}:{sec:02d}"


# ---------- Sidebar / Config ----------
st.sidebar.title("Configuration")
num_subteams = st.sidebar.number_input("Sub-teams per main team (X)", min_value=1, max_value=20, value=3, step=1)
if 'teams' not in st.session_state:
    init_state(num_subteams)

if st.sidebar.button("Reset all teams"):
    init_state(num_subteams)
    st.experimental_rerun()

st.sidebar.markdown("---")
st.sidebar.write("Click a Kill or Revive button to change a sub-team's state.")

# ---------- Main UI ----------
st.title("🔴 Alpha Team  —  🔵 Omega Team")
st.markdown("---")

col_alpha, col_omega = st.columns(2)

NOW = time.time()

# Render a team's panel
def render_team(column, team_name, color_hex):
    with column:
        # Team header with background color
        column.markdown(f"<div style='background:{color_hex}; padding:10px; border-radius:8px'>"
                        f"<h2 style='margin:0'>{team_name}</h2></div>", unsafe_allow_html=True)
        column.write("")

        subteams = st.session_state['teams'][team_name]
        for idx, st_obj in enumerate(subteams):
            name = st_obj['name']
            dead_until = st_obj.get('dead_until', 0.0)
            remaining = int(max(0, dead_until - NOW))
            status = "Dead" if remaining > 0 else "Alive"

            # Card for sub-team
            column.markdown(
                f"<div style='border:1px solid rgba(0,0,0,0.12); padding:8px; margin-bottom:8px; border-radius:6px'>"
                f"<b>{name}</b> — <i>{status}</i><br>")

            # roles
            roles_txt = ", ".join(st_obj['roles'])
            column.markdown(f"<small>Roles: {roles_txt}</small>", unsafe_allow_html=True)

            # show timer
            if remaining > 0:
                column.markdown(f"<div style='font-weight:700; font-size:18px'>Timer: {format_seconds(remaining)}</div>", unsafe_allow_html=True)
            else:
                column.markdown(f"<div style='color:green'><b>Ready</b></div>", unsafe_allow_html=True)

            # Buttons
            c1, c2 = column.columns([1,1])
            with c1:
                if st.button("Kill", key=f"kill_{team_name}_{idx}"):
                    st.session_state['teams'][team_name][idx]['dead_until'] = time.time() + 300
                    st.experimental_rerun()
            with c2:
                if st.button("Revive", key=f"revive_{team_name}_{idx}"):
                    st.session_state['teams'][team_name][idx]['dead_until'] = 0.0
                    st.experimental_rerun()

            column.markdown("</div>", unsafe_allow_html=True)


render_team(col_alpha, 'Alpha', '#ffcccc')
render_team(col_omega, 'Omega', '#cce7ff')

st.markdown("---")
st.info("Timers update on interaction or page refresh. If you want a live countdown, we can add auto-refresh.")

st.caption("Save this as app.py, run `pip install -r requirements.txt`, then `streamlit run app.py`.")
