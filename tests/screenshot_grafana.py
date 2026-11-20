#!/usr/bin/env python3
"""
Automated Grafana Screenshot Capture (Playwright)
Screenshots all three live dashboards for evidence.
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

EVIDENCE_DIR = Path("D:/MES/mes-project/evidence/A6")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

DASHBOARDS = [
    ("mes-d1-production-overview", "d1_production_overview.png", "Dashboard 1: Production Overview"),
    ("mes-d2-machine-monitoring", "d2_machine_monitoring.png", "Dashboard 2: Machine Monitoring"),
    ("mes-d3-production-analytics", "d3_production_analytics.png", "Dashboard 3: Production Analytics"),
]

def capture_screenshots():
    print("Launching Chromium browser via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        # 1. Login to Grafana
        print("Navigating to http://localhost:3000/login...")
        page.goto("http://localhost:3000/login", wait_until="networkidle")
        page.fill('input[name="user"]', "admin")
        page.fill('input[name="password"]', "admin")
        page.click('button[type="submit"]')
        time.sleep(3)
        
        # Check if skip prompt appears for password change
        skip_btn = page.query_selector('a:has-text("Skip"), button:has-text("Skip")')
        if skip_btn:
            skip_btn.click()
            time.sleep(2)
            
        print("Logged into Grafana successfully.")
        
        # 2. Capture each dashboard
        for uid, filename, title in DASHBOARDS:
            url = f"http://localhost:3000/d/{uid}?kiosk"
            print(f"Loading {title} at {url}...")
            page.goto(url, wait_until="networkidle")
            time.sleep(5)  # Wait for queries to execute and panels to render
            
            out_path = EVIDENCE_DIR / filename
            page.screenshot(path=str(out_path), full_page=True)
            print(f"Captured screenshot: {out_path} (size: {out_path.stat().st_size} bytes)")
            
        browser.close()
        print("All Grafana dashboard screenshots captured successfully!")

if __name__ == "__main__":
    capture_screenshots()
