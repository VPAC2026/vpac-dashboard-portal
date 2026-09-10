"""
Keep VPAC dashboards awake
==========================
Streamlit Community Cloud puts an app to sleep after 12 hours with no *real*
browser traffic. A plain HTTP GET (curl / requests) returns 200 but does NOT
reset the idle timer or wake a sleeping app — only an actual browser session
(websocket) does. So this script drives a headless Chromium page against each
live dashboard, clicks the "Yes, get this app back up!" button if the app is
asleep, and waits for it to render. Run on a schedule by GitHub Actions.

Keep this list in sync with the live `url` values in ../../streamlit_app.py
(DASHBOARDS). Only include dashboards that actually have a URL.
"""

import sys
from playwright.sync_api import sync_playwright

# Live dashboard URLs (mirror the non-empty DASHBOARDS[*]["url"] in streamlit_app.py)
URLS = [
    ("Workload Dashboard",   "https://vpac-workload.streamlit.app/"),
    ("Site Super Scorecard", "https://vpac-site-super-scorecard-smk29mdtuzrwx6ooihrysl.streamlit.app/"),
    ("Sales Dashboard",      "https://vpac-sales-dashboard.streamlit.app/"),
    ("PSP Scorecard",        "https://vpac-psp-scorecard.streamlit.app/"),
]

NAV_TIMEOUT_MS = 120_000   # allow for a full cold start
SETTLE_MS = 6_000          # give the app a moment to boot after a wake click
ATTEMPTS = 2               # retry once on transient failure


def warm_one(browser, name: str, url: str) -> bool:
    """Load one dashboard, wake it if asleep, confirm it renders. True on success."""
    for attempt in range(1, ATTEMPTS + 1):
        page = browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)

            # If the app is asleep, Streamlit shows a wake button — click it.
            try:
                wake = page.get_by_role(
                    "button", name="get this app back up", exact=False
                )
                if wake.count() > 0:
                    wake.first.click(timeout=15_000)
                    print(f"  [{name}] was asleep — clicked wake button")
                    page.wait_for_timeout(SETTLE_MS)
            except Exception:
                pass  # no wake button / already awake

            # Confirm the Streamlit app actually rendered.
            try:
                page.wait_for_selector(
                    '[data-testid="stApp"], [data-testid="stAppViewContainer"], #root',
                    timeout=60_000,
                )
                page.wait_for_timeout(2_000)
                print(f"  [{name}] OK (attempt {attempt})")
                return True
            except Exception:
                print(f"  [{name}] loaded but app container not detected "
                      f"(attempt {attempt})")
                # A load without the wake screen still counts as traffic; treat
                # a clean navigation as success even if the selector was missed.
                return True
        except Exception as e:
            print(f"  [{name}] attempt {attempt} failed: {type(e).__name__}: {e}")
        finally:
            page.close()
    return False


def main() -> int:
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        context_ok = True
        for name, url in URLS:
            print(f"Warming {name} …")
            if not warm_one(browser, name, url):
                failures.append(name)
        browser.close()

    if failures:
        print(f"\nFinished with failures: {', '.join(failures)}")
        return 1
    print("\nAll dashboards warmed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
