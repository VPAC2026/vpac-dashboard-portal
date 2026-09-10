# VPAC Dashboards — Unified Portal (Complete Dashboard)

## What this is
The single entry-point portal for all VPAC dashboards. It does **not** contain
the dashboards themselves — it gates access by person ("Who are you?" → "What
would you like to see?") and opens/embeds each dashboard's own Streamlit URL.

## How to run
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```
The portal is a single Streamlit file (`streamlit_app.py`). Dashboards open
embedded in a responsive full-viewport iframe, with an "Open in new tab"
fallback for password-protected or sleeping apps.

## Where to edit
Only the config block near the top of `streamlit_app.py`:
- **DASHBOARDS** — one entry per dashboard; paste each one's live URL (blank = "Coming soon").
- **PEOPLE** — who can open which dashboards (`"*"` = all).

## Dependencies
`streamlit>=1.35`. Also has `node_modules/` + `package.json` (jsdom etc.) for the HTML side.

## Connections / secrets
None. This portal only links out; no API tokens needed.

## Automation — keep dashboards awake
`.github/workflows/keep_awake.yml` runs `.github/scripts/keep_awake.py` every
3 hours (24/7, + manual dispatch). It drives a headless Chromium browser
against each live dashboard so Streamlit Community Cloud's 12h idle timer never
trips (a plain HTTP ping does NOT keep an app awake — only a real browser
session does). If you add/remove a live dashboard, update the `URLS` list in
`keep_awake.py` to match the DASHBOARDS block. No secrets required.

## GitHub
Repo: `VPAC2026/vpac-dashboard-portal` (public). Deploy on Streamlit Cloud,
branch `main`, main file `streamlit_app.py`. Local is linked and matches origin/main.

## Linked dashboards (URLs configured in the portal)
- Workload → https://vpac-workload.streamlit.app/
- Site Super Scorecard, Sales → live URLs set in DASHBOARDS block
- Forecasting, Assets → "Coming soon" (URLs blank)

## Open items
- Fill in Forecasting and Assets URLs when those dashboards go live.
- Add the PSP Scorecard as a portal entry if it should appear there.
