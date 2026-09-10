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

    # PSP Scorecard + Site Super access only
    "Justin Shudo":      ["psp_scorecard", "scorecard"],
    "Dexter Juric":      ["psp_scorecard", "scorecard"],
    "Justine Belanger":  ["psp_scorecard", "scorecard"],
    "Rayan Mohamed":     ["psp_scorecard", "scorecard"],
    "Adam Kasbar":       ["psp_scorecard", "scorecard"],
    "Dylan Galovich":    ["psp_scorecard", "scorecard"],
    "Jason Diao":        ["psp_scorecard", "scorecard"],
    "Paden Cuthill":     ["psp_scorecard", "scorecard"],
    "Ryan Stimson":      ["psp_scorecard", "scorecard"],
}

# =============================================================================
#  No edits needed below this line.
# =============================================================================

st.set_page_config(page_title="VPAC Dashboards", page_icon="\U0001F4CA", layout="wide")

VPAC_NAVY = "#143b66"

# ---------------------------------------------------------------------------
#  Global styling (portal landing page)
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
      .block-container {{ padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1180px; }}
      #MainMenu, footer {{ visibility: hidden; }}

      /* ---- Header banner ---- */
      .vpac-header {{
        background: linear-gradient(100deg, {VPAC_NAVY} 0%, #0f2c4d 100%);
        color: #fff; padding: 20px 26px; border-radius: 16px;
        display: flex; align-items: center; gap: 16px; margin-bottom: 8px;
        box-shadow: 0 10px 30px rgba(20,59,102,.18);
      }}
      .vpac-badge {{
        width: 48px; height: 48px; border-radius: 11px; background: #fff;
        color: {VPAC_NAVY}; font-weight: 800; font-size: 16px;
        display: flex; align-items: center; justify-content: center; letter-spacing: .5px;
        flex-shrink: 0;
      }}
      .vpac-header h1 {{ font-size: 21px; margin: 0; font-weight: 700; letter-spacing: .2px; }}
      .vpac-header p  {{ font-size: 12.5px; margin: 3px 0 0; opacity: .82; }}

      /* ---- Dashboard cards ---- */
      .dash-card {{
        border: 1px solid #e3e8ee; border-radius: 16px; padding: 22px 20px 16px;
        background: #fff; box-shadow: 0 8px 24px rgba(20,59,102,.07);
        min-height: 188px; position: relative; overflow: hidden;
        transition: transform .15s ease, box-shadow .15s ease;
      }}
      .dash-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 14px 34px rgba(20,59,102,.14);
      }}
      .dash-card.soon {{ opacity: .72; }}
      .dash-card .stripe {{ position:absolute; top:0; left:0; right:0; height:5px; }}
      .dash-ic {{ font-size: 30px; line-height: 1; }}
      .dash-card h3 {{ margin: 10px 0 5px; font-size: 16.5px; color: #16324f; }}
      .dash-card p {{ color: #6a7886; font-size: 12.6px; line-height: 1.55; margin: 0; }}
      .soon-tag {{ position:absolute; top:14px; right:14px;
        background:#94a3b8; color:#fff; font-size:10px;
        font-weight:700; letter-spacing:.6px; padding:3px 9px; border-radius:20px;
        text-transform:uppercase; }}

      /* Make the open/soon buttons sit flush under each card */
      div[data-testid="column"] .stButton > button {{
        border-radius: 10px; font-weight: 600; margin-top: 6px;
      }}

      .portal-caption {{ color:#6a7886; font-size:13px; margin: 2px 0 14px; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def allowed_for(person_name: str):
    sees = PEOPLE.get(person_name)
    if sees == "*":
        return list(DASHBOARDS.keys())
    return [d for d in (sees or []) if d in DASHBOARDS]


# ---------------------------------------------------------------------------
#  Embedded view  — a dashboard is open inside the portal
# ---------------------------------------------------------------------------
view = st.session_state.get("view")

# Resolve the person early so a page refresh keeps the embed valid.
person = st.session_state.get("who", "— Select your name —")

if view and person in PEOPLE and view in allowed_for(person) and DASHBOARDS[view]["url"]:
    d = DASHBOARDS[view]
    sep = "&" if "?" in d["url"] else "?"
    embed_url = d["url"] + sep + "embed=true"

    # Go full-bleed while a dashboard is open: kill padding, header, portal chrome.
    st.markdown(
        """
        <style>
          .block-container {max-width:100% !important;
            padding:0.5rem 1rem 0 !important;}
          .vpac-header {display:none;}
          header[data-testid="stHeader"] {height:0; min-height:0;}
          div[data-testid="stToolbar"] {display:none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    top = st.columns([1.4, 4.4, 1.4])
    with top[0]:
        if st.button("← Back to portal", use_container_width=True):
            st.session_state.pop("view", None)
            st.rerun()
    with top[1]:
        st.markdown(
            f"<div style='padding-top:6px;font-weight:600;color:{d['color']};"
            f"font-size:15px;'>{d['icon']} &nbsp;{d['title']}</div>",
            unsafe_allow_html=True,
        )
    with top[2]:
        st.link_button("Open in new tab ↗", d["url"], use_container_width=True)

    # Responsive, full-height embed.
    #   The dashboard is loaded in an iframe that JS stretches to fill the real
    #   browser viewport (not a fixed 1500px), so there's no dead whitespace and
    #   no awkward double-scroll. window.parent is same-origin (the Streamlit
    #   host) so reading innerHeight / resizing the frame element is allowed.
    components.html(
        f"""
        <div id="wrap" style="width:100%;">
          <iframe id="vpacframe"
                  src="{embed_url}"
                  title="{d['title']}"
                  style="width:100%; height:900px; border:0; border-radius:10px;
                         background:#f7f9fc;"
                  allow="clipboard-read; clipboard-write; fullscreen"></iframe>
          <div id="hint" style="font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
                                 color:#8a97a6; font-size:12px; text-align:center;
                                 margin-top:8px;">
            Seeing a login or a “waking up” screen? Use
            <b>Open in new tab</b> above — embedded views run as a separate session.
          </div>
        </div>
        <script>
          function fitVPAC() {{
            try {{
              var vh = window.parent.innerHeight || window.innerHeight;
              // Leave room for the top bar (~56px) and the hint line (~34px).
              var h = Math.max(520, vh - 150);
              var f = document.getElementById('vpacframe');
              if (f) f.style.height = h + 'px';
              // Stretch this component's own iframe so nothing gets clipped.
              if (window.frameElement) window.frameElement.style.height = (h + 46) + 'px';
            }} catch (e) {{ /* cross-origin or detached — ignore */ }}
          }}
          fitVPAC();
          window.addEventListener('resize', fitVPAC);
          if (window.parent) window.parent.addEventListener('resize', fitVPAC);
          setInterval(fitVPAC, 800);
        </script>
        """,
        height=980,
        scrolling=False,
    )
    st.stop()

# ---------------------------------------------------------------------------
#  Portal landing page
# ---------------------------------------------------------------------------
st.markdown(
    f"""
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

# ---- Step 2: What would you like to see today? ----
first = person.split()[0]
st.markdown(f"#### What would you like to see today, {first}?")

if not ids:
    st.warning("No dashboards are assigned to you yet. Contact Pratik to get access.")
    st.stop()

ready_count = sum(1 for i in ids if DASHBOARDS[i]["url"])
st.markdown(
    f"<div class='portal-caption'>You have access to {len(ids)} "
    f"dashboard{'s' if len(ids) != 1 else ''} "
    f"({ready_count} live). Click one to open it here in the portal.</div>",
    unsafe_allow_html=True,
)

cols = st.columns(3, gap="large")
for i, dash_id in enumerate(ids):
    d = DASHBOARDS[dash_id]
    ready = bool(d["url"])
    with cols[i % 3]:
        soon_tag = "" if ready else "<span class='soon-tag'>Coming soon</span>"
        st.markdown(
            f"""
            <div class="dash-card{'' if ready else ' soon'}">
              <div class="stripe" style="background:{d['color']}"></div>
              {soon_tag}
              <div class="dash-ic">{d['icon']}</div>
              <h3>{d['title']}</h3>
              <p>{d['desc']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if ready:
            if st.button("Open dashboard →", key=f"open_{dash_id}",
                         use_container_width=True, type="primary"):
                st.session_state["view"] = dash_id
                st.rerun()
        else:
            st.button("Coming soon", key=f"soon_{dash_id}", disabled=True,
                      use_container_width=True)
        st.write("")
