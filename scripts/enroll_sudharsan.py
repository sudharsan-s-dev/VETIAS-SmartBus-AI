"""
Enroll Sudharsan S into Database with extracted facial embedding from ERP photo
"""

import os
import sys
import json
import cv2

# Ensure parent directory is on sys.path for app and vision_helper imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db, Student
import vision_helper

def enroll_sudharsan():
    photo_filename = "file_000000000ae48211946ea01f6e5ab888 - Sudharsan.png"
    photo_path = os.path.join(ROOT_DIR, "static", "uploads", "erp_photos", photo_filename)

    if not os.path.exists(photo_path):
        print(f"[ERROR] Photo file not found at {photo_path}")
        return

    img = cv2.imread(photo_path)
    if img is None:
        print(f"[ERROR] Failed to read image from {photo_path}")
        return

    status, result = vision_helper.process_image_for_embedding(img)
    if status != 'SUCCESS':
        print(f"[ERROR] Face detection failed on photo: {result}")
        return

    embedding_vector = result
    print(f"[SUCCESS] Extracted {len(embedding_vector)}-D face embedding vector from photo.")

    with app.app_context():
        # Check if student exists by ID, Email, or Name
        student = Student.query.filter(
            (Student.student_id_str == '24AID62') |
            (Student.email == 'sudharsan15052007@gmail.com') |
            (Student.name == 'Sudharsan S')
        ).first()

        if not student:
            student = Student(
                name='Sudharsan S',
                email='sudharsan15052007@gmail.com',
                student_id_str='24AID62',
                phone='9876543210',
                department='B.Sc Computer Science (AI & Data Science)',
                year='3rd Year',
                semester='Semester 5',
                bus_no='Bus-06',
                parent_name='Parent of Sudharsan',
                parent_email='sudharsan15052007@gmail.com',
                parent_phone='9876543210',
                fee_status='Paid',
                password='pass'
            )
            db.session.add(student)
            db.session.commit()
            print(f"[DB] Created new Student record for Sudharsan S (ID: {student.id}).")
        else:
            student.name = 'Sudharsan S'
            student.email = 'sudharsan15052007@gmail.com'
            student.student_id_str = '24AID62'
            student.department = 'B.Sc Computer Science (AI & Data Science)'
            student.year = '3rd Year'
            student.semester = 'Semester 5'
            student.bus_no = 'Bus-06'
            student.parent_email = 'sudharsan15052007@gmail.com'
            print(f"[DB] Found existing Student record for Sudharsan S (ID: {student.id}). Updating...")

        student.face_embedding = json.dumps(embedding_vector)
        student.face_enrolled = True

        # Copy image for standardized admin ERP photo access
        erp_save_path = os.path.join("static", "uploads", "erp_photos", f"student_{student.id}.jpg")
        cv2.imwrite(erp_save_path, img)

        db.session.commit()

        print("===============================================================")
        print(f"  [SUCCESS] Sudharsan S (ID: {student.id} | Roll: 24AID62)  ")
        print(f"  Facial Vector Enrolled Successfully in Database!           ")
        print("===============================================================")

if __name__ == "__main__":
    enroll_sudharsan()
