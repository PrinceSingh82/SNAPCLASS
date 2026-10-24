import streamlit as st
import time
import numpy as np
from PIL import Image

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier,
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendence,
    unenroll_student_to_subject,
)
from src.components.dialog_enroll import enroll_dialog
from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.components.subject_card import subject_card


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    # Open the Quick Enrollment dialog when requested
    if st.session_state.get("open_quick_enroll"):
        join_code = st.session_state.get("pending_join_code")

        # Mark this code as handled before opening the dialog
        st.session_state["open_quick_enroll"] = False

        if join_code:
            st.session_state["join_dialog_handled_for"] = join_code
            auto_enroll_dialog(join_code)
            return

    # Header
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {student_data['name']}")

        if st.button(
            "Logout",
            type="secondary",
            key="student_logout_btn",
            shortcut="control+backspace",
        ):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("student_data", None)
            st.session_state.pop("user_role", None)
            st.session_state["login_type"] = None
            st.session_state.pop("open_quick_enroll", None)
            st.session_state.pop("pending_join_code", None)
            st.session_state.pop("join_dialog_handled_for", None)
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)

    with c1:
        st.header("Your Enrolled Subjects")

    with c2:
        if st.button(
            "Enroll in subjects",
            type="primary",
            width="stretch",
        ):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your enrolled subjects.."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendence(student_id)

    # Attendance statistics
    stats_map = {}

    for log in logs:
        sid = log["subject_id"]

        if sid not in stats_map:
            stats_map[sid] = {
                "total": 0,
                "attended": 0,
            }

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    # Subject cards
    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]

        stats = stats_map.get(
            sid,
            {"total": 0, "attended": 0},
        )

        def unenroll_button(
            subject_id=sid,
            subject_name=sub["name"],
        ):
            if st.button(
                "Unenroll from this course",
                type="tertiary",
                width="stretch",
                icon=":material/delete_forever:",
            ):
                unenroll_student_to_subject(
                    student_id,
                    subject_id,
                )
                st.toast(
                    f"Unenrolled from {subject_name} successfully"
                )
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("🗓️", "Total", stats["total"]),
                    ("✅", "Attended", stats["attended"]),
                ],
                footer_callback=unenroll_button,
            )

    footer_dashboard()


# =========================================================
# STUDENT SCREEN
# =========================================================

def student_screen():
    style_background_dashboard()
    style_base_layout()

    # Read the join code from URLs such as ?join-code=CS204
    join_code = st.query_params.get("join-code")

    if join_code:
        handled_code = st.session_state.get("join_dialog_handled_for")

        if handled_code != join_code:
            st.session_state["pending_join_code"] = join_code

            # If the student is already logged in, open the dialog
            if st.session_state.get("student_data"):
                st.session_state["open_quick_enroll"] = True

    # If already logged in
    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Header
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
        ):
            st.session_state["login_type"] = None
            st.session_state.pop("pending_join_code", None)
            st.session_state.pop("open_quick_enroll", None)
            st.rerun()

    st.header(
        "Login using FaceID",
        text_alignment="center",
    )
    st.write("")

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    show_registration = False

    # Face login
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

        if num_faces == 0:
            st.warning(
                "Face not found! Please position your face properly."
            )

        elif num_faces > 1:
            st.warning(
                "Multiple faces found! Please keep only one face "
                "in front of the camera."
            )

        else:
            # Recognized student
            if detected:
                student_id = list(detected.keys())[0]
                all_students = get_all_students()

                student = next(
                    (
                        s for s in all_students
                        if int(s["student_id"]) == int(student_id)
                    ),
                    None,
                )

                if student:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_role"] = "student"
                    st.session_state["student_data"] = student

                    st.toast(
                        f"Welcome back {student['name']}!"
                    )
                    time.sleep(1)

                    if st.session_state.get("pending_join_code"):
                        st.session_state["open_quick_enroll"] = True

                    st.rerun()

                else:
                    st.error(
                        "Student record not found in database."
                    )

            else:
                st.info(
                    "Face not recognized! You might be a new student."
                )
                show_registration = True

    # =====================================================
    # NEW STUDENT REGISTRATION
    # =====================================================

    if show_registration:
        with st.container(border=True):
            st.header("Register New Profile")

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Prince Singh",
            )

            st.subheader("Optional: Voice Enrollment")
            st.info(
                "Enroll your voice for voice-based attendance."
            )

            audio_data = None

            try:
                audio_data = st.audio_input(
                    "Record a short phrase like: "
                    "I am present, my name is Prince."
                )
            except Exception:
                st.error("Audio recording is not available.")

            if st.button("Create Account", type="primary"):
                if not new_name.strip():
                    st.warning("Please enter your name!")

                else:
                    with st.spinner("Creating profile..."):
                        # Generate face embedding
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)

                        if not encodings:
                            st.error(
                                "Couldn't capture your facial features."
                            )

                        else:
                            face_embedding = encodings[0].tolist()

                            # Voice embedding
                            voice_embedding = None

                            if audio_data:
                                voice_embedding = get_voice_embedding(
                                    audio_data.read()
                                )

                            # Save student
                            response_data = create_student(
                                name=new_name.strip(),
                                face_embedding=face_embedding,
                                voice_embedding=voice_embedding,
                            )

                            if response_data:
                                train_classifier()
                                student = response_data[0]

                                st.session_state["is_logged_in"] = True
                                st.session_state["user_role"] = "student"
                                st.session_state["student_data"] = student

                                st.toast(
                                    f"Welcome {student['name']}!"
                                )
                                time.sleep(1)

                                if st.session_state.get("pending_join_code"):
                                    st.session_state["open_quick_enroll"] = True

                                st.rerun()

                            else:
                                st.error(
                                    "Unable to create student profile."
                                )

    footer_dashboard()
