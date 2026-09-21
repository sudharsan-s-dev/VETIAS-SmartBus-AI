"""
Vision Helper Module for VETIAS SmartBus AI (Phase 1)
------------------------------------------------------
Provides MediaPipe-based face detection, 1404-dimensional facial landmark embedding 
extraction, distance matching, EAR blink calculation, and base64/image file processing.
"""

import os
import json
import numpy as np
import cv2

try:
    import mediapipe as mp
except ImportError:
    mp = None

# Ensure face_landmarker.task model is available
MODEL_PATH = os.path.join(os.path.dirname(__file__), "face_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        import urllib.request
        try:
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        except Exception as e:
            print(f"[ERROR] Failed downloading face_landmarker.task: {e}")

# EAR Indices
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133

RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
RIGHT_EYE_LEFT = 362
RIGHT_EYE_RIGHT = 263

EAR_CLOSED_THRESHOLD = 0.19
EAR_OPEN_THRESHOLD = 0.23

_landmarker_detector = None

def get_detector():
    global _landmarker_detector
    if _landmarker_detector is not None:
        return _landmarker_detector

    ensure_model()
    try:
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=5 # Allow detecting multiple faces to reject multi-face enrollment
        )
        landmarker = vision.FaceLandmarker.create_from_options(options)

        def detect_fn(cv2_bgr_img):
            rgb = cv2.cvtColor(cv2_bgr_img, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = landmarker.detect(mp_img)
            if not result.face_landmarks:
                return []
            return [l.landmark if hasattr(l, 'landmark') else l for l in result.face_landmarks]

        _landmarker_detector = detect_fn
        return _landmarker_detector
    except Exception as e:
        print(f"[VISION HELPER] Tasks API fallback: {e}")
        try:
            mp_face_mesh = mp.solutions.face_mesh
            mesh = mp_face_mesh.FaceMesh(max_num_faces=5, refine_landmarks=True)
            def detect_fn_sol(cv2_bgr_img):
                rgb = cv2.cvtColor(cv2_bgr_img, cv2.COLOR_BGR2RGB)
                res = mesh.process(rgb)
                if not res.multi_face_landmarks:
                    return []
                return [l.landmark for l in res.multi_face_landmarks]
            _landmarker_detector = detect_fn_sol
            return _landmarker_detector
        except Exception as e2:
            raise RuntimeError(f"MediaPipe initialization error: {e2}")

try:
    import onnxruntime as ort
except ImportError:
    ort = None

ONNX_MODEL_PATH = os.path.join(os.path.dirname(__file__), "mobilefacenet.onnx")
_onnx_session = None

# Standard InsightFace 112x112 5-point reference landmarks
REFERENCE_5PTS = np.array([
    [38.2946, 51.6963],  # Left eye center
    [73.5318, 51.5014],  # Right eye center
    [56.0252, 71.7366],  # Nose tip
    [41.5493, 92.3655],  # Left mouth corner
    [70.7299, 92.2041]   # Right mouth corner
], dtype=np.float32)

def get_onnx_session():
    global _onnx_session
    if _onnx_session is not None:
        return _onnx_session
    if not os.path.exists(ONNX_MODEL_PATH):
        raise FileNotFoundError(f"ONNX model file not found: {ONNX_MODEL_PATH}")
    if ort is None:
        raise RuntimeError("onnxruntime module is not installed.")
    _onnx_session = ort.InferenceSession(ONNX_MODEL_PATH)
    return _onnx_session

def extract_deep_embedding_from_landmarks(cv2_bgr_img, landmarks):
    """
    Uses MediaPipe 5 key points (refined pupil centers, nose tip, mouth corners) to perform 
    affine alignment to 112x112, then passes tensor through MobileFaceNet ONNX for 512-D L2-normalized embedding.
    """
    h, w, _ = cv2_bgr_img.shape

    def get_pt(idx):
        lm = landmarks[idx]
        if hasattr(lm, 'x'):
            return np.array([lm.x * w, lm.y * h], dtype=np.float32)
        return np.array([lm[0] * w, lm[1] * h], dtype=np.float32)

    # Use pupil landmarks 468 and 473 for sub-pixel eye alignment when available
    if len(landmarks) >= 474:
        left_eye = get_pt(468)
        right_eye = get_pt(473)
    else:
        left_eye = (get_pt(33) + get_pt(133)) / 2.0
        right_eye = (get_pt(362) + get_pt(263)) / 2.0

    nose = get_pt(1)
    left_mouth = get_pt(61)
    right_mouth = get_pt(291)

    src_pts = np.array([left_eye, right_eye, nose, left_mouth, right_mouth], dtype=np.float32)

    # Estimate similarity transformation matrix
    M, _ = cv2.estimateAffinePartial2D(src_pts, REFERENCE_5PTS)
    if M is None:
        aligned = cv2.resize(cv2_bgr_img, (112, 112))
    else:
        aligned = cv2.warpAffine(cv2_bgr_img, M, (112, 112), borderValue=0)

    rgb = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
    blob = (rgb.astype(np.float32) - 127.5) / 127.5
    blob = np.transpose(blob, (2, 0, 1))
    blob = np.expand_dims(blob, axis=0)

    session = get_onnx_session()
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    outputs = session.run([output_name], {input_name: blob})
    vec = outputs[0][0]
    norm = np.linalg.norm(vec) + 1e-6
    return (vec / norm).tolist()

def process_image_for_embedding(cv2_img):
    """
    Detects faces in OpenCV BGR image using MediaPipe, crops/aligns, and extracts 512-D ONNX embedding.
    Returns:
       (status_code, result_data)
       status_code: 'SUCCESS', 'NO_FACE', or 'MULTIPLE_FACES'
       result_data: list float embedding vector if SUCCESS, else error string
    """
    detector = get_detector()
    face_list = detector(cv2_img)

    if len(face_list) == 0:
        return 'NO_FACE', 'No face detected in the photo.'
    elif len(face_list) > 1:
        return 'MULTIPLE_FACES', 'Multiple faces detected. Please ensure only one face is in the photo.'

    landmarks = face_list[0]
    embedding = extract_deep_embedding_from_landmarks(cv2_img, landmarks)
    return 'SUCCESS', embedding

def calculate_ear_from_landmarks(landmarks, width, height):
    def get_pt(idx):
        lm = landmarks[idx]
        return np.array([lm.x * width, lm.y * height])

    left_top = get_pt(LEFT_EYE_TOP)
    left_bot = get_pt(LEFT_EYE_BOTTOM)
    left_left = get_pt(LEFT_EYE_LEFT)
    left_right = get_pt(LEFT_EYE_RIGHT)
    left_v = np.linalg.norm(left_top - left_bot)
    left_h = np.linalg.norm(left_left - left_right)
    left_ear = left_v / (left_h + 1e-6)

    right_top = get_pt(RIGHT_EYE_TOP)
    right_bot = get_pt(RIGHT_EYE_BOTTOM)
    right_left = get_pt(RIGHT_EYE_LEFT)
    right_right = get_pt(RIGHT_EYE_RIGHT)
    right_v = np.linalg.norm(right_top - right_bot)
    right_h = np.linalg.norm(right_left - right_right)
    right_ear = right_v / (right_h + 1e-6)

    return (left_ear + right_ear) / 2.0

def compute_vector_distance(vec1, vec2):
    v1 = np.array(vec1, dtype=np.float32)
    v2 = np.array(vec2, dtype=np.float32)

    min_len = min(len(v1), len(v2))
    if min_len > 0:
        v1 = v1[:min_len]
        v2 = v2[:min_len]
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        if n1 > 1e-6: v1 = v1 / n1
        if n2 > 1e-6: v2 = v2 / n2

    cos_sim = float(np.dot(v1, v2))
    cos_dist = float(1.0 - cos_sim)
    return cos_dist, cos_sim
