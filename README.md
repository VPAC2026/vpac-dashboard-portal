# VPAC Dashboards — Unified Portal

One entry point for every VPAC dashboard, gated by person.

**Flow:** *Who are you?* → *What would you like to see today?* → opens the
dashboard that person is allowed to see.

This portal does **not** contain the dashboards themselves. Each dashboard is
its own Streamlit app / GitHub repo. The portal only controls **who sees what**
and links out to each dashboard's URL.

## Files
- `streamlit_app.py` — the portal (deployed on Streamlit Cloud).
- `index.html` — the same portal as a standalone HTML file (double-click to run locally; no server needed).
- `requirements.txt` — Python dependencies.

## Edit the config
Open `streamlit_app.py` and edit the two blocks near the top:
- **DASHBOARDS** — add/remove dashboards and paste each one's live URL.
- **PEOPLE** — add/remove people and set which dashboards each can open (`"*"` = all).

Keep `index.html` in sync if you use both.

## Deploy on Streamlit Cloud
1. Push this repo to GitHub (e.g. `VPAC2026/vpac-dashboard-portal`).
2. Go to https://share.streamlit.io → **New app**.
3. Pick this repo, branch `main`, main file `streamlit_app.py` → **Deploy**.
4. Copy the app's URL — that's the single link you share with the whole team.

## Related repos (the individual dashboards)
- `VPAC2026/vpac-workload` — Workload
- `VPAC2026/vpac-sales-dashboard` — Sales
- `VPAC2026/vpac-site-super-scorecard` — Scorecard
- `VPAC2026/vpac-psp-scorecard` — Scorecard (PSP)
