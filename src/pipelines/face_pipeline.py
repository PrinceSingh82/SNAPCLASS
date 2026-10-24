import dlib
import numpy as np
import face_recognition_models
import streamlit as st

from sklearn.svm import SVC
from src.database.db import get_all_students


# =========================================================
# LOAD DLIB FACE MODELS
# =========================================================

@st.cache_resource
def load_dlib_models():

    # Face detector
    detector = dlib.get_frontal_face_detector()

    # Shape predictor
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    # Face recognition model
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


# =========================================================
# GENERATE FACE EMBEDDINGS
# =========================================================

def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    # Detect faces
    faces = detector(image_np, 1)

    encodings = []

    for face in faces:

        # Get facial landmarks
        shape = sp(image_np, face)

        # Generate 128-dimensional face embedding
        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(
            np.array(face_descriptor, dtype=np.float64)
        )

    return encodings


# =========================================================
# TRAIN SVM CLASSIFIER
# =========================================================

@st.cache_resource
def get_trained_model():

    X_train = []
    y_train = []

    # Get students from database
    student_db = get_all_students()

    if not student_db:
        return None

    # Collect embeddings
    for student in student_db:

        embedding = student.get("face_embedding")

        if embedding:

            X_train.append(
                np.array(embedding, dtype=np.float64)
            )

            y_train.append(
                student.get("student_id")
            )

    # No face embeddings available
    if len(X_train) == 0:
        return None

    # Convert to numpy arrays
    X_train = np.array(X_train)
    y_train = np.array(y_train)

    # Get unique students
    all_students = sorted(
        list(set(y_train.tolist()))
    )

    # -----------------------------------------------------
    # SVM requires at least 2 classes
    # -----------------------------------------------------

    clf = None

    if len(all_students) >= 2:

        clf = SVC(
            kernel="linear",
            probability=True,
            class_weight="balanced"
        )

        try:
            clf.fit(X_train, y_train)

        except ValueError:
            clf = None

    return {
        "clf": clf,
        "X": X_train,
        "y": y_train
    }


# =========================================================
# RETRAIN CLASSIFIER
# =========================================================

def train_classifier():

    st.cache_resource.clear()

    model_data = get_trained_model()

    return model_data is not None


# =========================================================
# PREDICT ATTENDANCE
# =========================================================

def predict_attendance(class_image_np):

    # Get face embeddings from camera image
    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    # Train/load model
    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    # All registered students
    all_students = sorted(
        list(set(y_train.tolist()))
    )

    if len(all_students) == 0:
        return detected_students, [], len(encodings)

    # Face matching threshold
    resemblance_threshold = 0.6

    # -----------------------------------------------------
    # Process every detected face
    # -----------------------------------------------------

    for encoding in encodings:

        predicted_id = None

        # -------------------------------------------------
        # If 2 or more students exist, use SVM
        # -------------------------------------------------

        if clf is not None:

            prediction = clf.predict(
                [encoding]
            )

            predicted_id = int(prediction[0])

        # -------------------------------------------------
        # If only one student exists
        # -------------------------------------------------

        else:

            predicted_id = int(
                all_students[0]
            )

        # -------------------------------------------------
        # Find embeddings belonging to predicted student
        # -------------------------------------------------

        student_indices = np.where(
            y_train == predicted_id
        )[0]

        if len(student_indices) == 0:
            continue

        # -------------------------------------------------
        # Compare with all embeddings of that student
        # -------------------------------------------------

        distances = []

        for index in student_indices:

            student_embedding = X_train[index]

            distance = np.linalg.norm(
                student_embedding - encoding
            )

            distances.append(distance)

        # Best match
        best_match_score = min(distances)

        # -------------------------------------------------
        # Threshold check
        # -------------------------------------------------

        if best_match_score <= resemblance_threshold:

            detected_students[predicted_id] = True

    return (
        detected_students,
        all_students,
        len(encodings)
    )


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================
# Agar tumhare kisi purane code mein
# predict_attendence() likha hua hai,
# to woh bhi kaam karega.

def predict_attendence(class_image_np):

    return predict_attendance(class_image_np)