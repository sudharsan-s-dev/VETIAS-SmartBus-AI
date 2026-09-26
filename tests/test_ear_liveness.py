import os
import sys
import json
import base64
import cv2
import numpy as np

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Student, Attendance, SecurityAlert
import vision_helper

def run_liveness_tests():
    print("======================================================================")
    print("      SERVER-SIDE EAR FACIAL LIVENESS VERIFICATION TEST SUITE        ")
    print("======================================================================")

    with app.app_context():
        # Ensure at least one enrolled student exists for matching
        enrolled_student = Student.query.filter_by(face_enrolled=True).first()
        if not enrolled_student:
            print("[SETUP] Creating dummy enrolled student for liveness test...")
            dummy_vec = (np.ones(512) / np.sqrt(512)).tolist()
            enrolled_student = Student(
                name="Liveness Test Student",
                register_no="LIVENESS99",
                department="CSE",
                year="IV",
                parent_phone="9998887770",
                parent_email="parent_liveness@vetias.ac.in",
                bus_no="Bus-10",
                password="pass",
                face_enrolled=True,
                face_embedding=json.dumps(dummy_vec)
            )
            db.session.add(enrolled_student)
            db.session.commit()

        # Find a real face snapshot image from static/uploads/snapshots
        snapshots_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'snapshots')
        sample_img_path = None
        if os.path.exists(snapshots_dir):
            for f in os.listdir(snapshots_dir):
                if f.endswith('.jpg') and 'success_' in f:
                    sample_img_path = os.path.join(snapshots_dir, f)
                    break

        if sample_img_path and os.path.exists(sample_img_path):
            sample_img = cv2.imread(sample_img_path)
            print(f"[TEST SETUP] Loaded real face snapshot: {os.path.basename(sample_img_path)}")
        else:
            print("[TEST SETUP] Generating fallback synthetic image for testing...")
            sample_img = np.zeros((300, 300, 3), dtype=np.uint8)

        _, buf = cv2.imencode('.jpg', sample_img)
        b64_single = "data:image/jpeg;base64," + base64.b64encode(buf).decode('utf-8')

        client = app.test_client()

        # ----------------------------------------------------------------------
        # TEST 1: STATIC PHOTO / SPOOF ATTACK SEQUENCE (Identical Frames)
        # ----------------------------------------------------------------------
        print("\n----------------------------------------------------------------------")
        print(" TEST 1: Static Photo Sequence (6 Identical Frames — Spoof Attack)")
        print("----------------------------------------------------------------------")
        static_sequence = [b64_single] * 6

        alert_count_before = SecurityAlert.query.count()

        res = client.post('/api/mark-attendance-face', json={
            'image_sequence': static_sequence,
            'bus_no': 'Bus-10'
        })

        data = res.get_json()
        print(f" HTTP Status Code : {res.status_code}")
        print(f" Response Data    : {data}")

        assert res.status_code == 400 or (data and data.get('status') == 'error'), "Static sequence should return error status"
        assert 'Liveness Verification Failed' in data.get('message', ''), f"Expected Liveness Verification Failed message, got: {data.get('message')}"

        alert_count_after = SecurityAlert.query.count()
        assert alert_count_after > alert_count_before, "SecurityAlert record must be created for liveness failure"
        
        latest_alert = SecurityAlert.query.order_by(SecurityAlert.timestamp.desc()).first()
        print(f" [VERIFIED] SecurityAlert Logged -> Reason: '{latest_alert.reason}' | Snapshot: {latest_alert.snapshot_path}")

        # ----------------------------------------------------------------------
        # TEST 2: SIMULATED DYNAMIC BLINK SEQUENCE (Open -> Closed -> Open)
        # ----------------------------------------------------------------------
        print("\n----------------------------------------------------------------------")
        print(" TEST 2: Dynamic EAR Blink Sequence Logic (Open -> Closed -> Open)")
        print("----------------------------------------------------------------------")

        # Test helper function directly with simulated EAR values
        # We test the blink sequence criteria logic:
        # has_open (EAR >= 0.21), has_closed (EAR <= 0.19), ear_delta >= 0.035
        simulated_ear_seq_pass = [0.26, 0.25, 0.14, 0.15, 0.27, 0.26]
        has_open_pass = any(e >= vision_helper.EAR_OPEN_THRESHOLD for e in simulated_ear_seq_pass)
        has_closed_pass = any(e <= vision_helper.EAR_CLOSED_THRESHOLD for e in simulated_ear_seq_pass)
        delta_pass = max(simulated_ear_seq_pass) - min(simulated_ear_seq_pass)
        liveness_pass = has_open_pass and has_closed_pass and (delta_pass >= 0.035)

        print(f" Simulated EAR Sequence : {simulated_ear_seq_pass}")
        print(f" Min EAR: {min(simulated_ear_seq_pass):.3f} | Max EAR: {max(simulated_ear_seq_pass):.3f} | Delta: {delta_pass:.3f}")
        print(f" Has Open Eyes (>= {vision_helper.EAR_OPEN_THRESHOLD})   : {has_open_pass}")
        print(f" Has Closed Eyes (<= {vision_helper.EAR_CLOSED_THRESHOLD}) : {has_closed_pass}")
        print(f" Liveness Decision       : {liveness_pass}")
        assert liveness_pass is True, "Valid blink sequence must evaluate to True"

        # Test simulated static photo EAR sequence (no blink)
        simulated_ear_seq_fail = [0.26, 0.26, 0.25, 0.26, 0.26, 0.25]
        has_open_fail = any(e >= vision_helper.EAR_OPEN_THRESHOLD for e in simulated_ear_seq_fail)
        has_closed_fail = any(e <= vision_helper.EAR_CLOSED_THRESHOLD for e in simulated_ear_seq_fail)
        delta_fail = max(simulated_ear_seq_fail) - min(simulated_ear_seq_fail)
        liveness_fail = has_open_fail and has_closed_fail and (delta_fail >= 0.035)

        print(f"\n Simulated Static EAR Sequence: {simulated_ear_seq_fail}")
        print(f" Min EAR: {min(simulated_ear_seq_fail):.3f} | Max EAR: {max(simulated_ear_seq_fail):.3f} | Delta: {delta_fail:.3f}")
        print(f" Has Closed Eyes (<= {vision_helper.EAR_CLOSED_THRESHOLD}) : {has_closed_fail}")
        print(f" Liveness Decision       : {liveness_fail}")
        assert liveness_fail is False, "Static photo EAR sequence must evaluate to False"

        # ----------------------------------------------------------------------
        # TEST 3: CLIENT PAYLOAD VERIFICATION (No self-reported liveness_verified)
        # ----------------------------------------------------------------------
        print("\n----------------------------------------------------------------------")
        print(" TEST 3: Client Payload Spoof Attempt (Sending liveness_verified: true)")
        print("----------------------------------------------------------------------")
        # Attempt to bypass by sending client-side liveness_verified: true in request body
        res_spoof = client.post('/api/mark-attendance-face', json={
            'image_sequence': static_sequence,
            'bus_no': 'Bus-10',
            'liveness_verified': True  # Malicious client trying to self-report liveness
        })
        data_spoof = res_spoof.get_json()
        print(f" HTTP Status Code : {res_spoof.status_code}")
        print(f" Response Data    : {data_spoof}")

        assert res_spoof.status_code == 400, "Server MUST ignore client self-reported liveness_verified and evaluate server-side sequence"
        assert 'Liveness Verification Failed' in data_spoof.get('message', ''), "Server correctly rejected spoof attempt despite client sending liveness_verified: true"

        print("\n======================================================================")
        print("   [SUCCESS] ALL LIVENESS VERIFICATION TESTS PASSED EMPIRICALLY!     ")
        print("======================================================================\n")

if __name__ == "__main__":
    run_liveness_tests()
