import os
import sys
import csv
import json
import cv2
from werkzeug.security import generate_password_hash

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app, db, Student
from vision_helper import process_image_for_embedding

PARENT_EMAIL = "sudharsanselvarajj@gmail.com"
PARENT_PHONE = "+91 8610547273"
CSV_PATH = os.path.join(PROJECT_ROOT, "enrollment_data", "form_responses.csv")
PHOTOS_DIR = os.path.join(PROJECT_ROOT, "demo_photos")

def resize_if_needed(img, max_dim=1280):
    if img is None:
        return None
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / float(max(h, w))
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img

def seed_and_enroll():
    if not os.path.exists(CSV_PATH):
        print(f"[ERROR] CSV file not found at: {CSV_PATH}")
        return

    print("==========================================================")
    print("   SEED AND ENROLL DEMO STUDENTS (LOCAL DB ONLY)")
    print("==========================================================")
    print(f"Parent Email : {PARENT_EMAIL}")
    print(f"Parent Phone : {PARENT_PHONE}")
    print(f"CSV Source   : {CSV_PATH}")
    print(f"Photos Dir   : {PHOTOS_DIR}")
    print("----------------------------------------------------------\n")

    summary_rows = []

    with app.app_context():
        # Read form responses CSV
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_id = row.get("Student ID", "").strip()
                if not raw_id:
                    continue
                
                student_id_str = raw_id.upper()
                name = row.get("Full Name", "").strip()
                department = row.get("Department", "").strip()
                year = row.get("Year", "").strip()
                semester = row.get("Semester", "").strip()
                bus_no = row.get("Bus Number", "").strip().upper()
                email = row.get("Email Address", "").strip().lower()

                # Check if student already exists by student_id_str
                student = Student.query.filter_by(student_id_str=student_id_str).first()

                created_new = False
                if not student:
                    student = Student(
                        name=name,
                        student_id_str=student_id_str,
                        email=email,
                        department=department,
                        year=f"{year}, {semester}",
                        semester=semester,
                        bus_no=bus_no,
                        parent_email=PARENT_EMAIL,
                        parent_phone=PARENT_PHONE,
                        phone="+91 0000000000 (Demo)",
                        address="Demo data - not provided",
                        password=generate_password_hash("demo1234"),
                        fee_status="Paid",
                        device_id=None
                    )
                    db.session.add(student)
                    created_new = True
                else:
                    # Update existing record fields
                    student.name = name
                    student.email = email
                    student.department = department
                    student.year = f"{year}, {semester}"
                    student.semester = semester
                    student.bus_no = bus_no
                    student.parent_email = PARENT_EMAIL
                    student.parent_phone = PARENT_PHONE

                db.session.flush() # Ensure student.id is available

                # Locate matching photo in demo_photos directory
                photo_file = None
                for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]:
                    candidate = os.path.join(PHOTOS_DIR, f"{student_id_str}{ext}")
                    if os.path.exists(candidate):
                        photo_file = candidate
                        break

                face_enrolled = False
                notes = ""

                if photo_file:
                    cv2_img = cv2.imread(photo_file)
                    if cv2_img is not None:
                        cv2_img_proc = resize_if_needed(cv2_img)
                        status, result = process_image_for_embedding(cv2_img_proc)
                        if status == 'SUCCESS':
                            student.face_embedding = json.dumps(result)
                            student.face_enrolled = True
                            face_enrolled = True
                            notes = f"Enrolled successfully ({os.path.basename(photo_file)})"
                        else:
                            notes = f"Embedding failed: {result}"
                    else:
                        notes = f"Could not read image file: {photo_file}"
                else:
                    notes = f"No photo found for {student_id_str} in demo_photos/"

                summary_rows.append({
                    "roll": student_id_str,
                    "name": name,
                    "created": "Yes" if created_new else "No (Updated)",
                    "enrolled": "Yes" if face_enrolled else "No",
                    "notes": notes
                })

        db.session.commit()

        # Print Summary Table
        print("\n==========================================================================================================")
        print("                                       PROCESSING SUMMARY TABLE")
        print("==========================================================================================================")
        print(f"{'ROLL NO':<12} | {'NAME':<24} | {'NEW ROW?':<12} | {'FACE ENROLLED?':<14} | {'NOTES'}")
        print("-" * 106)
        for r in summary_rows:
            print(f"{r['roll']:<12} | {r['name']:<24} | {r['created']:<12} | {r['enrolled']:<14} | {r['notes']}")
        print("==========================================================================================================\n")

        # Verification Step
        print("==========================================================")
        print("               VERIFICATION & AUDIT REPORT")
        print("==========================================================")
        all_students = Student.query.order_by(Student.id).all()
        print(f"Total Student records in local DB: {len(all_students)}\n")
        print(f"{'ID':<4} | {'ROLL NO':<12} | {'NAME':<24} | {'PARENT EMAIL':<30} | {'FACE ENROLLED'}")
        print("-" * 90)
        for s in all_students:
            print(f"{s.id:<4} | {str(s.student_id_str):<12} | {s.name:<24} | {str(s.parent_email):<30} | {s.face_enrolled}")
        print("==========================================================\n")

if __name__ == "__main__":
    seed_and_enroll()
