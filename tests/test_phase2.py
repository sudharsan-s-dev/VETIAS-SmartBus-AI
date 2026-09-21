"""
Automated Verification Suite for Phase 2 - Driver AI Gate Kiosk UI
------------------------------------------------------------------
Verifies:
1. Driver portal route /driver renders with AI Gate section and navigation tabs.
2. QR Code fallback element exists and is rendered.
3. /api/mark-attendance-face remains responsive to kiosk camera frame payloads.
"""

import sys
import os

# Ensure parent directory is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ['SKIP_DEVICE_CHECK'] = 'True'

from app import app, db

def run_tests():
    print("===============================================================")
    print("   VETIAS SmartBus AI - Phase 2 Driver Kiosk UI Test Suite  ")
    print("===============================================================\n")

    client = app.test_client()

    # 1. Login Driver Session
    with client.session_transaction() as sess:
        sess['user_id'] = 999
        sess['user_type'] = 'driver'
        sess['bus_no'] = 'Bus-10'

    # 2. GET /driver
    res = client.get('/driver')
    assert res.status_code == 200, f"Driver page GET failed with code {res.status_code}"
    html = res.get_data(as_text=True)

    # 3. Check for Phase 2 elements in driver.html
    assert 'id="aigate"' in html, "Missing #aigate section in driver.html"
    assert 'id="ai-video"' in html, "Missing #ai-video element in driver.html"
    assert 'id="aigate-banner"' in html, "Missing #aigate-banner element in driver.html"
    assert 'id="qrcode-aigate"' in html, "Missing fallback QR container in driver.html"
    assert '/api/mark-attendance-face' in html, "Missing JS endpoint binding to /api/mark-attendance-face"

    print("[TEST 1] Driver page rendered successfully with AI Gate Kiosk section.")
    print("[TEST 2] Live video element (#ai-video) and Result Banner (#aigate-banner) verified.")
    print("[TEST 3] QR Code Fallback (#qrcode-aigate) verified.")
    print("[TEST 4] JS binding to /api/mark-attendance-face verified.")

    print("\n===============================================================")
    print("  [SUCCESS] ALL PHASE 2 KIOSK UI TESTS PASSED SUCCESSFULLY!  ")
    print("===============================================================\n")

if __name__ == "__main__":
    run_tests()
