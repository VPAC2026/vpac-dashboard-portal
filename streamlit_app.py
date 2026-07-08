"""
VPAC Dashboards — Unified Portal (one continuous app)
=====================================================
One entry point for every VPAC dashboard, gated by person.

Flow:  Who are you?  ->  What would you like to see today?  ->  the chosen
dashboard opens EMBEDDED inside this portal, with a "Back to portal" button.

This app does NOT contain the dashboards themselves. Each dashboard is its own
Streamlit app (its own repo / URL). This portal only decides WHO can see WHICH
dashboard, and embeds them.

------------------------------------------------------------------------------
EDIT ONLY THE CONFIG BLOCK BELOW.
------------------------------------------------------------------------------
"""

import streamlit as st
import streamlit.components.v1 as components

# =============================================================================
# 1) DASHBOARDS  — one entry per dashboard.
#    url : the live Streamlit Cloud link. Leave "" if not ready -> "Coming soon".
# =============================================================================
DASHBOARDS = {
    "workload": {
        "title": "Workload Dashboard",
        "desc":  "Team capacity, budgeted vs target hours, and role-level workload roll-ups.",
        "icon":  "\U0001F4CA",      # 📊
        "color": "#1f6fc4",
        "url":   "https://vpac-workload.streamlit.app/",
    },
    "scorecard": {
        "title": "Site Super Scorecard",
        "desc":  "Site superintendent scorecards, KPI submissions, and quarterly performance.",
        "icon":  "\U0001F3AF",      # 🎯
        "color": "#2b9348",
        "url":   "https://vpac-site-super-scorecard-smk29mdtuzrwx6ooihrysl.streamlit.app/",
    },
    "sales": {
        "title": "Sales Dashboard",
        "desc":  "Pipeline, pace-to-goal, new build pre-con, and fiscal-year sales performance.",
        "icon":  "\U0001F4C8",      # 📈
        "color": "#e07a1f",
        "url":   "https://vpac-sales-dashboard.streamlit.app/",
    },
    "forecasting": {
        "title": "Forecasting Dashboard",
        "desc":  "Revenue and project forecasting — coming soon.",
        "icon":  "\U0001F52E",      # 🔮
        "color": "#7b4fc9",
        "url":   "",  # leave blank -> "Coming soon"
    },
    "assets": {
        "title": "Assets Dashboard",
        "desc":  "Equipment and asset tracking, utilization, and maintenance status.",
        "icon":  "\U0001F3D7️",  # 🏗️
        "color": "#0d9488",
        "url":   "",  # leave blank -> "Coming soon"
    },
    "psp_scorecard": {
        "title": "PSP Scorecard",
        "desc":  "Project Support Person scorecards, KPI submissions, and performance tracking.",
        "icon":  "\U0001F4CB",      # 📋
        "color": "#c0392b",
        "url":   "https://vpac-psp-scorecard.streamlit.app/",
    },
    # To add another dashboard later, copy a block above and give it a new id.
}


def all_but(*exclude):
    """Every dashboard id except the ones listed. Auto-includes future dashboards."""
    return [d for d in DASHBOARDS if d not in exclude]


# =============================================================================
# 2) PEOPLE  — one entry per person.
#    "sees" = "*" for all, a list of dashboard ids, or all_but("sales", ...).
# =============================================================================
PEOPLE = {
    "Pratik Pakhale":    "*",                                   # everything
    "Warren Bakk":       "*",                                   # everything
    "Ben Bakk":          "*",                                   # everything
    "Brady Irwin":       ["workload", "scorecard", "sales"],
    "Cassie Glover":     all_but("sales"),                      # everything but Sales
    "Nathan Kalenuik":   all_but("sales"),                      # everything but Sales
    "Gerhard Booysen":   all_but("sales"),                      # everything but Sales
    "Marguerite Butler": all_but("sales"),                      # everything but Sales
    "Sina Jafarian":     ["psp_scorecard", "sales"],
    "Kash Shafiei":      ["assets", "psp_scorecard", "workload"],
}

# =============================================================================
#  No edits needed below this line.
# =============================================================================

st.set_page_config(page_title="VPAC Dashboards", page_icon="\U0001F4CA", layout="wide")

VPAC_NAVY = "#143b66"

st.markdown(
    f"""
    <style>
      .block-container {{ padding-top: 1.6rem; max-width: 1150px; }}
      #MainMenu, footer {{ visibility: hidden; }}
      .vpac-header {{
        background: linear-gradient(100deg, {VPAC_NAVY} 0%, #0f2c4d 100%);
        color: #fff; padding: 18px 24px; border-radius: 14px;
        display: flex; align-items: center; gap: 16px; margin-bottom: 22px;
      }}
      .vpac-badge {{
        width: 44px; height: 44px; border-radius: 10px; background: #fff;
        color: {VPAC_NAVY}; font-weight: 800; font-size: 15px;
        display: flex; align-items: center; justify-content: center; letter-spacing: .5px;
      }}
      .vpac-header h1 {{ font-size: 20px; margin: 0; font-weight: 700; }}
      .vpac-header p  {{ font-size: 12.5px; margin: 2px 0 0; opacity: .82; }}
      .dash-card {{
        border: 1px solid #e3e8ee; border-radius: 16px; padding: 20px 20px 12px;
        background: #fff; box-shadow: 0 8px 24px rgba(20,59,102,.08);
        min-height: 176px; position: relative;
      }}
      .dash-card .stripe {{ position:absolute; top:0; left:0; right:0; height:5px;
        border-radius: 16px 16px 0 0; }}
      .dash-ic {{ font-size: 28px; }}
      .dash-card h3 {{ margin: 6px 0 4px; font-size: 16.5px; }}
      .dash-card p {{ color: #6a7886; font-size: 12.5px; line-height: 1.5; margin: 0; }}
      .soon-tag {{ display:inline-block; background:#94a3b8; color:#fff; font-size:10.5px;
        font-weight:600; letter-spacing:.5px; padding:3px 9px; border-radius:20px;
        text-transform:uppercase; }}
    </style>
    <div class="vpac-header">
      <div class="vpac-badge">VPAC</div>
      <div>
        <h1>VPAC Dashboards</h1>
        <p>Construction Group &middot; Internal Reporting Portal</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def allowed_for(person_name: str):
    sees = PEOPLE.get(person_name)
    if sees == "*":
        return list(DASHBOARDS.keys())
    return [d for d in (sees or []) if d in DASHBOARDS]


# ---- Step 1: Who are you? ----
person = st.selectbox(
    "Who are you?",
    ["— Select your name —"] + sorted(PEOPLE.keys()),
    key="who",
)

if person == "— Select your name —":
    st.session_state.pop("view", None)
    st.info("Select your name above to see the dashboards assigned to you.")
    st.stop()

ids = allowed_for(person)

# ---- Embedded view: a dashboard is open inside the portal ----
view = st.session_state.get("view")
if view and view in ids and DASHBOARDS[view]["url"]:
    d = DASHBOARDS[view]
    top = st.columns([1.4, 6])
    with top[0]:
        if st.button("← Back to portal", use_container_width=True):
            st.session_state.pop("view", None)
            st.rerun()
    with top[1]:
        st.markdown(
            f"<div style='padding-top:6px;font-weight:600;color:{d['color']}'>"
            f"{d['icon']} &nbsp;{d['title']}</div>",
            unsafe_allow_html=True,
        )
    sep = "&" if "?" in d["url"] else "?"
    components.iframe(d["url"] + sep + "embed=true", height=1100, scrolling=True)
    st.stop()

# ---- Step 2: What would you like to see today? ----
first = person.split()[0]
st.markdown(f"#### What would you like to see today, {first}?")

if not ids:
    st.warning("No dashboards are assigned to you yet. Contact Pratik to get access.")
    st.stop()

st.caption(
    f"You have access to {len(ids)} dashboard{'s' if len(ids) != 1 else ''}. "
    "Click one to open it here."
)

cols = st.columns(3)
for i, dash_id in enumerate(ids):
    d = DASHBOARDS[dash_id]
    ready = bool(d["url"])
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="dash-card">
              <div class="stripe" style="background:{d['color']}"></div>
              <div class="dash-ic">{d['icon']}</div>
              <h3>{d['title']}</h3>
              <p>{d['desc']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if ready:
            if st.button("Open dashboard →", key=f"open_{dash_id}",
                         use_container_width=True):
                st.session_state["view"] = dash_id
                st.rerun()
        else:
            st.button("Coming soon", key=f"soon_{dash_id}", disabled=True,
                      use_container_width=True)
        st.write("")
