# import streamlit as st


# # =========================================================
# # UI
# # =========================================================

# from src.ui.base_layout import (
#     style_background_dashboard,
#     style_base_layout
# )

# from src.components.header import header_dashboard
# from src.components.footer import footer_dashboard


# # =========================================================
# # DATABASE
# # =========================================================

# from src.database.db import (
#     check_teacher_exists,
#     create_teacher,
#     teacher_login,
#     get_teacher_subjects
# )


# # =========================================================
# # DIALOGS
# # =========================================================

# from src.components.dialog_create_subject import (
#     create_subject_dialog
# )

# from src.components.dialog_share_subject import (
#     share_subject_dialog
# )

# from src.components.subject_card import subject_card
# from src.components.dialog_add_photo import add_photos_dialog
# from src.components.dialog_add_photos import add_photos_dialog

# from src.pipelines.face_pipeline import predict_attnedence
# import numpy as np
# from src.database.config import supabase
# from datetime import datetime
# import pandas as pd
# from src.components.dialog_attendance_results import attendence_result_dialog

# # =========================================================
# # TEACHER SCREEN
# # =========================================================

# def teacher_screen():

#     style_background_dashboard()
#     style_base_layout()

#     # -----------------------------------------------------
#     # Teacher already logged in
#     # -----------------------------------------------------

#     if "teacher_data" in st.session_state:

#         teacher_dashboard()

#     # -----------------------------------------------------
#     # Login screen
#     # -----------------------------------------------------

#     elif (
#         "teacher_login_type" not in st.session_state
#         or st.session_state.teacher_login_type == "login"
#     ):

#         teacher_screen_login()

#     # -----------------------------------------------------
#     # Register screen
#     # -----------------------------------------------------

#     elif st.session_state.teacher_login_type == "register":

#         teacher_screen_register()


# # =========================================================
# # TEACHER DASHBOARD
# # =========================================================

# def teacher_dashboard():

#     teacher_data = st.session_state.teacher_data

#     # -----------------------------------------------------
#     # HEADER
#     # -----------------------------------------------------

#     c1, c2 = st.columns(
#         2,
#         vertical_alignment="center",
#         gap="xxlarge"
#     )

#     # -----------------------------------------------------
#     # LEFT SIDE
#     # -----------------------------------------------------

#     with c1:

#         header_dashboard()

#     # -----------------------------------------------------
#     # RIGHT SIDE
#     # -----------------------------------------------------

#     with c2:

#         st.subheader(
#             f"Welcome, {teacher_data['name']}"
#         )

#         if st.button(
#             "Logout",
#             type="secondary",
#             key="teacher_logout_btn",
#             shortcut="control+backspace"
#         ):

#             st.session_state["is_logged_in"] = False

#             st.session_state.pop(
#                 "teacher_data",
#                 None
#             )

#             st.session_state.pop(
#                 "user_role",
#                 None
#             )

#             st.session_state.teacher_login_type = "login"

#             st.rerun()

#     st.space()

#     # -----------------------------------------------------
#     # DEFAULT TAB
#     # -----------------------------------------------------

#     if "current_teacher_tab" not in st.session_state:

#         st.session_state.current_teacher_tab = (
#             "take_attendance"
#         )

#     # -----------------------------------------------------
#     # THREE TABS
#     # -----------------------------------------------------

#     tab1, tab2, tab3 = st.columns(3)

#     # =====================================================
#     # TAKE ATTENDANCE
#     # =====================================================

#     with tab1:

#         button_type = (
#             "primary"
#             if st.session_state.current_teacher_tab
#             == "take_attendance"
#             else "tertiary"
#         )

#         if st.button(
#             "Take Attendance",
#             type=button_type,
#             width="stretch",
#             icon=":material/ar_on_you:",
#             key="take_attendance_btn"
#         ):

#             st.session_state.current_teacher_tab = (
#                 "take_attendance"
#             )

#             st.rerun()

#     # =====================================================
#     # MANAGE SUBJECTS
#     # =====================================================

#     with tab2:

#         button_type = (
#             "primary"
#             if st.session_state.current_teacher_tab
#             == "manage_subjects"
#             else "tertiary"
#         )

#         if st.button(
#             "Manage Subjects",
#             type=button_type,
#             width="stretch",
#             icon=":material/book_ribbon:",
#             key="manage_subjects_btn"
#         ):

#             st.session_state.current_teacher_tab = (
#                 "manage_subjects"
#             )

#             st.rerun()

#     # =====================================================
#     # ATTENDANCE RECORDS
#     # =====================================================

#     with tab3:

#         button_type = (
#             "primary"
#             if st.session_state.current_teacher_tab
#             == "attendance_records"
#             else "tertiary"
#         )

#         if st.button(
#             "Attendance Records",
#             type=button_type,
#             width="stretch",
#             icon=":material/cards_stack:",
#             key="attendance_records_btn"
#         ):

#             st.session_state.current_teacher_tab = (
#                 "attendance_records"
#             )

#             st.rerun()

#     st.divider()

#     # =====================================================
#     # TAB CONTENT
#     # =====================================================

#     if (
#         st.session_state.current_teacher_tab
#         == "take_attendance"
#     ):

#         teacher_tab_take_attendance()

#     elif (
#         st.session_state.current_teacher_tab
#         == "manage_subjects"
#     ):

#         teacher_tab_manage_subjects()

#     elif (
#         st.session_state.current_teacher_tab
#         == "attendance_records"
#     ):

#         teacher_tab_attendance_records()

#     footer_dashboard()


# # =========================================================
# # TAKE ATTENDANCE TAB
# # =========================================================


# def teacher_tab_take_attendance():
#     teacher_id = st.session_state.teacher_data["teacher_id"]

#     st.header("Take AI Attendance")
#     st.info("AI attendance system will appear here.")

#     # Initialize attendance images
#     if "attendance_images" not in st.session_state:
#         st.session_state.attendance_images = []

#     subjects = get_teacher_subjects(teacher_id)

#     if not subjects:
#         st.warning(
#             "You haven't created any subject yet! "
#             "Please create one to begin!"
#         )
#         return

#     # Subject dropdown options
#     subject_options = {
#         f"{s['name']} - {s['subject_id']}": s["subject_id"]
#         for s in subjects
#     }

#     col1, col2 = st.columns([3, 1])

#     with col1:
#         selected_subject_label = st.selectbox(
#             "Select Subjects",
#             options=list(subject_options.keys()),
#         )

#     with col2:
#         if st.button(
#             "Add Photos",
#             type="primary",
#             icon=":material/photo_prints:",
#             width="stretch",
#         ):
#             add_photos_dialog()

#     # Get the selected subject ID
#     selected_subject_id = subject_options[selected_subject_label]

#     st.divider()

#     if st.sesssion_state.attendance_images:
#         st.header("Added Photos")
#         gallery_cols = st.columns(4)

#         for idx, img in enumerate(st.session_state.attendance_images):
#             with gallery_cols[idx % 4]:
#                 st.image(img, width="stretch", caption=f"photo {idx+1}")


#         c1, c2, c3 = st.columns(3)
#         with c1:
#             if st.button("Clear all photos" , width = "stretch", type="tertiary", icon=":material/delete:"):
#                 st.session_state.attendance_images = []
#                 st.rerun()

#         with c2:
#             has_photos = bool(st.session_state.attendecne_images)
#             if st.button("Run Face Analysis ", width="stretch", type="secondary", icon=':material/analytics:'):
#                 with st.spinner("Deep scanning classroom phtos..."):
#                     imp_np = np.array(img.convert("RGB"))

#                     detected, _, _ = predict_attendence(img_np)

#                     if detected:
#                         for sid in detected.keys():
#                             student_id = int(sid)

#                             all_detected_id.setdefault(student_id, []).append(f"photo{idx+1}")

#                 enrolled_res = supabase.table("subject_students").select("*, students(*)").eq("subject_id", selected_subject_id).execute()
#                 enrolled_students = enrolled_res.data

#                 if not enrolled_students:
#                     st.warning("No student enrolled in this course")
#                 else:
#                     results, attendence_to_log =[],[]

#                     current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

#                     for node in enrolled_students:
#                         student = node["students"]
#                         sources = all_detected_ids.get(int(student["student_id"]),[])
#                         is_present = len(sources) > 0

#                         result.append({
#                             "Name": student["name"],
#                             "ID": student["student_id"],
#                             "Sources": ",".join(sources) if is_present else "-",
#                             "Status": "✅ Present" if is present else" ❌ Absent"

#                         })

#                         attendence_to_log.append({
#                             "student_id": student["student_id"],
#                             "subject_id":selected_subject_id,
#                             "timestamp": current_timestamp,
#                             "is_present": bool(is_present)
#                         })

#                 attendence_result_dialog(pd.DataFrame(results), attendence_to_log)

#         with c3:
#             st.button("Use Voice Attendence", type="primary", width="stretch", icon = ":material/mic:"):
#             voice_attendence_dialog()





#     # The selected ID is now available for attendance processing.
#     # Actual AI attendance processing can be added here.



    
        




# # =========================================================
# # MANAGE SUBJECTS TAB
# # =========================================================

# def teacher_tab_manage_subjects():

#     teacher_id = st.session_state.teacher_data["teacher_id"]

#     # -----------------------------------------------------
#     # HEADER
#     # -----------------------------------------------------

#     col1, col2 = st.columns(
#         [1, 1.2],
#         vertical_alignment="center"
#     )

#     with col1:

#         st.header(
#             "Manage Subjects"
#         )

#     with col2:

#         if st.button(
#             "Create New Subject",
#             width="stretch",
#             key="create_subject_btn"
#         ):

#             create_subject_dialog(
#                 teacher_id
#             )

#     st.divider()

#     # -----------------------------------------------------
#     # GET SUBJECTS
#     # -----------------------------------------------------

#     subjects = get_teacher_subjects(
#         teacher_id
#     )

#     # -----------------------------------------------------
#     # SUBJECTS FOUND
#     # -----------------------------------------------------

#     if subjects:

#         for sub in subjects:

#             subject_name = sub.get(
#                 "name",
#                 "Unknown Subject"
#             )

#             subject_code = sub.get(
#                 "subject_code",
#                 "N/A"
#             )

#             section = sub.get(
#                 "section",
#                 "N/A"
#             )

#             total_students = sub.get(
#                 "total_students",
#                 0
#             )

#             total_classes = sub.get(
#                 "total_classes",
#                 0
#             )

#             # =================================================
#             # WHITE SUBJECT CARD
#             # =================================================

#             with st.container(
#                 border=True
#             ):

#                 # -------------------------------------------------
#                 # SUBJECT NAME
#                 # -------------------------------------------------

#                 st.subheader(
#                     subject_name
#                 )

#                 # -------------------------------------------------
#                 # CODE + SECTION
#                 # -------------------------------------------------

#                 st.write(
#                     f"**Code:** `{subject_code}`  |  "
#                     f"**Section:** `{section}`"
#                 )

#                 # -------------------------------------------------
#                 # STUDENTS + CLASSES
#                 # -------------------------------------------------

#                 stat1, stat2 = st.columns(2)

#                 with stat1:

#                     st.metric(
#                         "👥 Students",
#                         total_students
#                     )

#                 with stat2:

#                     st.metric(
#                         "⏰ Classes",
#                         total_classes
#                     )

#             # =================================================
#             # SHARE CODE BUTTON
#             # =================================================

#             if st.button(
#                 f"🔗 Share Code: {subject_name}",
#                 type="secondary",
#                 key=f"share_{subject_code}",
#                 width="content"
#             ):

#                 share_subject_dialog(
#                     sub
#                 )

#             st.write("")

#     # -----------------------------------------------------
#     # NO SUBJECTS
#     # -----------------------------------------------------

#     else:

#         st.info(
#             "NO SUBJECT FOUND. CREATE ONE ABOVE."
#         )


# # =========================================================
# # ATTENDANCE RECORDS TAB
# # =========================================================

# def teacher_tab_attendance_records():

#     st.header(
#         "Attendance Records"
#     )

#     st.info(
#         "Attendance records will appear here."
#     )


# # =========================================================
# # TEACHER LOGIN FUNCTION
# # =========================================================

# def login_teacher(
#     username,
#     password
# ):

#     if not username or not password:

#         return False

#     teacher = teacher_login(
#         username,
#         password
#     )

#     if teacher:

#         st.session_state.user_role = "teacher"

#         st.session_state.teacher_data = teacher

#         st.session_state.is_logged_in = True

#         return True

#     return False


# # =========================================================
# # TEACHER LOGIN SCREEN
# # =========================================================

# def teacher_screen_login():

#     c1, c2 = st.columns(
#         2,
#         vertical_alignment="center",
#         gap="xxlarge"
#     )

#     # -----------------------------------------------------
#     # LEFT SIDE
#     # -----------------------------------------------------

#     with c1:

#         header_dashboard()

#     # -----------------------------------------------------
#     # RIGHT SIDE
#     # -----------------------------------------------------

#     with c2:

#         if st.button(
#             "Go back to Home",
#             type="secondary",
#             key="teacher_login_back_btn",
#             shortcut="control+backspace"
#         ):

#             st.session_state["login_type"] = None

#             st.rerun()

#     st.header(
#         "Login using password",
#         text_alignment="center"
#     )

#     st.space()
#     st.space()

#     teacher_username = st.text_input(
#         "Enter username",
#         placeholder="ananyaroy"
#     )

#     teacher_pass = st.text_input(
#         "Enter password",
#         type="password",
#         placeholder="Enter your password"
#     )

#     st.divider()

#     btnc1, btnc2 = st.columns(2)

#     # -----------------------------------------------------
#     # LOGIN
#     # -----------------------------------------------------

#     with btnc1:

#         if st.button(
#             "Login",
#             icon=":material/passkey:",
#             shortcut="control+enter",
#             width="stretch",
#             key="teacher_login_btn"
#         ):

#             if login_teacher(
#                 teacher_username,
#                 teacher_pass
#             ):

#                 st.toast(
#                     "Welcome back!"
#                 )

#                 st.rerun()

#             else:

#                 st.error(
#                     "Invalid username or password"
#                 )

#     # -----------------------------------------------------
#     # REGISTER
#     # -----------------------------------------------------

#     with btnc2:

#         if st.button(
#             "Register Instead",
#             type="primary",
#             icon=":material/passkey:",
#             shortcut="control+enter",
#             width="stretch",
#             key="teacher_register_btn"
#         ):

#             st.session_state.teacher_login_type = (
#                 "register"
#             )

#             st.rerun()

#     footer_dashboard()


# # =========================================================
# # REGISTER TEACHER FUNCTION
# # =========================================================

# def register_teacher(
#     teacher_username,
#     teacher_name,
#     teacher_pass,
#     teacher_pass_confirm
# ):

#     # -----------------------------------------------------
#     # REQUIRED FIELDS
#     # -----------------------------------------------------

#     if (
#         not teacher_username
#         or not teacher_name
#         or not teacher_pass
#         or not teacher_pass_confirm
#     ):

#         return (
#             False,
#             "All fields are required!"
#         )

#     # -----------------------------------------------------
#     # USERNAME CHECK
#     # -----------------------------------------------------

#     if check_teacher_exists(
#         teacher_username
#     ):

#         return (
#             False,
#             "Username already taken"
#         )

#     # -----------------------------------------------------
#     # PASSWORD CONFIRMATION
#     # -----------------------------------------------------

#     if teacher_pass != teacher_pass_confirm:

#         return (
#             False,
#             "Passwords don't match"
#         )

#     # -----------------------------------------------------
#     # CREATE TEACHER
#     # -----------------------------------------------------

#     try:

#         create_teacher(
#             teacher_username,
#             teacher_pass,
#             teacher_name
#         )

#         return (
#             True,
#             "Successfully created! Login now."
#         )

#     except Exception as e:

#         print(
#             "Registration error:",
#             e
#         )

#         return (
#             False,
#             "Unexpected error!"
#         )


# # =========================================================
# # TEACHER REGISTER SCREEN
# # =========================================================

# def teacher_screen_register():

#     c1, c2 = st.columns(
#         2,
#         vertical_alignment="center",
#         gap="xxlarge"
#     )

#     # -----------------------------------------------------
#     # LEFT SIDE
#     # -----------------------------------------------------

#     with c1:

#         header_dashboard()

#     # -----------------------------------------------------
#     # RIGHT SIDE
#     # -----------------------------------------------------

#     with c2:

#         if st.button(
#             "Go back to Home",
#             type="secondary",
#             key="teacher_register_back_btn",
#             shortcut="control+backspace"
#         ):

#             st.session_state.teacher_login_type = (
#                 "login"
#             )

#             st.rerun()

#     st.header(
#         "Register Your Teacher Profile",
#         text_alignment="center"
#     )

#     st.space()
#     st.space()

#     teacher_username = st.text_input(
#         "Enter username",
#         placeholder="ananyaroy"
#     )

#     teacher_name = st.text_input(
#         "Enter name",
#         placeholder="Ananya Roy"
#     )

#     teacher_pass = st.text_input(
#         "Enter password",
#         type="password",
#         placeholder="Enter your password"
#     )

#     teacher_pass_confirm = st.text_input(
#         "Confirm your password",
#         type="password",
#         placeholder="Enter your password"
#     )

#     st.divider()

#     btnc1, btnc2 = st.columns(2)

#     # -----------------------------------------------------
#     # REGISTER
#     # -----------------------------------------------------

#     with btnc1:

#         if st.button(
#             "Register Now",
#             icon=":material/passkey:",
#             shortcut="control+enter",
#             width="stretch",
#             key="teacher_register_now_btn"
#         ):

#             success, message = register_teacher(
#                 teacher_username,
#                 teacher_name,
#                 teacher_pass,
#                 teacher_pass_confirm
#             )

#             if success:

#                 st.success(
#                     message
#                 )

#                 import time

#                 time.sleep(2)

#                 st.session_state.teacher_login_type = (
#                     "login"
#                 )

#                 st.rerun()

#             else:

#                 st.error(
#                     message
#                 )

#     # -----------------------------------------------------
#     # LOGIN
#     # -----------------------------------------------------

#     with btnc2:

#         if st.button(
#             "Login Instead",
#             type="primary",
#             icon=":material/passkey:",
#             shortcut="control+enter",
#             width="stretch",
#             key="teacher_login_instead_btn"
#         ):

#             st.session_state.teacher_login_type = (
#                 "login"
#             )

#             st.rerun()

#     footer_dashboard()



import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# =========================================================
# UI
# =========================================================

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

# =========================================================
# DATABASE
# =========================================================

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher
)

from src.database.config import supabase

# =========================================================
# DIALOGS
# =========================================================

from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photos_dialog

# Correct function name from face_pipeline.py
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
# =========================================================
# TEACHER SCREEN
# =========================================================

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


# =========================================================
# TEACHER DASHBOARD
# =========================================================

def teacher_dashboard():

    teacher_data = st.session_state.teacher_data

    # HEADER
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        st.subheader(
            f"Welcome, {teacher_data.get('name', 'Teacher')}"
        )

        if st.button(
            "Logout",
            type="secondary",
            key="teacher_logout_btn",
            shortcut="control+backspace",
        ):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("teacher_data", None)
            st.session_state.pop("user_role", None)
            st.session_state["teacher_login_type"] = "login"
            st.session_state.pop("current_teacher_tab", None)
            st.rerun()

    st.space()

    # DEFAULT TAB
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    # THREE TABS
    tab1, tab2, tab3 = st.columns(3)

    # TAKE ATTENDANCE
    with tab1:

        button_type = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "tertiary"
        )

        if st.button(
            "Take Attendance",
            type=button_type,
            width="stretch",
            icon=":material/ar_on_you:",
            key="take_attendance_btn",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    # MANAGE SUBJECTS
    with tab2:

        button_type = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "tertiary"
        )

        if st.button(
            "Manage Subjects",
            type=button_type,
            width="stretch",
            icon=":material/book_ribbon:",
            key="manage_subjects_btn",
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    # ATTENDANCE RECORDS
    with tab3:

        button_type = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "tertiary"
        )

        if st.button(
            "Attendance Records",
            type=button_type,
            width="stretch",
            icon=":material/cards_stack:",
            key="attendance_records_btn",
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    # TAB CONTENT
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


# =========================================================
# TAKE ATTENDANCE TAB
# =========================================================

def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.header("Take AI Attendance")
    st.info("Add classroom photos to analyze student attendance.")

    # Keep the existing session-state key used by the photo dialog.
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning(
            "You haven't created any subject yet! "
            "Please create one to begin!"
        )
        return

    # Subject dropdown
    subject_options = {
        f"{subject['name']} - {subject['subject_id']}":
            subject["subject_id"]
        for subject in subjects
    }

    col1, col2 = st.columns([3, 1],vertical_alignment = "bottom")

    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys()),
            key="attendance_subject_select",
        )

    with col2:
        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch",
            key="add_attendance_photos_btn",
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # Display photos
    images = st.session_state.attendance_images

    if not images:
        st.info("No photos added yet. Click 'Add Photos' to begin.")
    else:
        st.subheader("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(images):
            with gallery_cols[idx % 4]:
                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}",
                )
    has_photos=bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    # CLEAR PHOTOS
    with c1:
        if st.button(
            "Clear All Photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled= not has_photos,
            key="clear_attendance_photos_btn",
        ):
            st.session_state.attendance_images = []
            st.rerun()

    # RUN FACE ANALYSIS
    with c2:
    
        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            key="run_face_analysis_btn",
        ):

            all_detected_ids = {}

            with st.spinner("Scanning classroom photos..."):
                try:
                    # Analyze every uploaded photo.
                    for idx, img in enumerate(images):

                        img_np = np.array(img.convert("RGB"))

                        detected, _, _ = predict_attendance(img_np)

                        if detected:
                            for sid in detected.keys():

                                student_id = int(sid)

                                all_detected_ids.setdefault(
                                    student_id, []
                                ).append(f"Photo {idx + 1}")

                    # Fetch students enrolled in the selected subject.
                    enrolled_res = (
                        supabase.table("subject_students")
                        .select("*, students(*)")
                        .eq("subject_id", selected_subject_id)
                        .execute()
                    )

                    enrolled_students = enrolled_res.data or []

                    if not enrolled_students:
                        st.warning(
                            "No students are enrolled in this subject."
                        )
                        return

                    results = []
                    attendance_to_log = []

                    current_timestamp = datetime.now().isoformat()

                    # Prepare attendance results.
                    for node in enrolled_students:

                        student = node.get("students")

                        if not student:
                            continue

                        student_id = int(student["student_id"])

                        sources = all_detected_ids.get(
                            student_id, []
                        )

                        is_present = bool(sources)

                        results.append({
                            "Name": student.get("name", "Unknown"),
                            "ID": student_id,
                            "Sources": (
                                ", ".join(sources)
                                if is_present
                                else "-"
                            ),
                            "Status": (
                                "Present ✅ "
                                if is_present
                                else "Absent ❌"
                            ),
                        })

                        attendance_to_log.append({
                            "student_id": student_id,
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": is_present,
                        })

                    if results:
                        attendance_result_dialog(
                            pd.DataFrame(results),
                            attendance_to_log,
                        )
                    else:
                        st.warning(
                            "No valid enrolled student records were found."
                        )

                except Exception as e:
                    st.error(f"Face analysis failed: {e}")

    # VOICE ATTENDANCE
    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:",
            key="voice_attendance_btn",
        ):
             
            voice_attendance_dialog(selected_subject_id)
            # st.info(
            #     "Voice attendance has not been implemented yet."
            # )


# =========================================================
# MANAGE SUBJECTS TAB
# =========================================================

def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    # HEADER
    col1, col2 = st.columns(
        [1, 1.2],
        vertical_alignment="center",
    )

    with col1:
        st.header("Manage Subjects")

    with col2:
        if st.button(
            "Create New Subject",
            width="stretch",
            key="create_subject_btn",
        ):
            create_subject_dialog(teacher_id)

    st.divider()

    # GET SUBJECTS
    subjects = get_teacher_subjects(teacher_id)

    # SUBJECTS FOUND
    if subjects:

        for sub in subjects:

            subject_name = sub.get(
                "name",
                "Unknown Subject",
            )

            subject_code = sub.get(
                "subject_code",
                "N/A",
            )

            section = sub.get(
                "section",
                "N/A",
            )

            total_students = sub.get(
                "total_students",
                0,
            )

            total_classes = sub.get(
                "total_classes",
                0,
            )

            # WHITE SUBJECT CARD
            with st.container(border=True):

                st.subheader(subject_name)

                st.write(
                    f"**Code:** `{subject_code}`  |  "
                    f"**Section:** `{section}`"
                )

                stat1, stat2 = st.columns(2)

                with stat1:
                    st.metric(
                        "👥 Students",
                        total_students,
                    )

                with stat2:
                    st.metric(
                        "⏰ Classes",
                        total_classes,
                    )

            # SHARE CODE BUTTON
            if st.button(
                f"🔗 Share Code: {subject_name}",
                type="secondary",
                key=f"share_{subject_code}",
                width="content",
            ):
                share_subject_dialog(sub)

            st.write("")

    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE.")


# =========================================================
# ATTENDANCE RECORDS TAB
# =========================================================

def teacher_tab_attendance_records():

    st.header("Attendance Records")

    st.info("Attendance records will appear here.")

    teacher_id = st.session_state.teacher_data["teacher_id"]

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return
    data = []
    for r in records:
        ts = r.get("timestamp")

    data.append({
        "ts_group": ts.split(" ")[0] if ts else None,
        "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
        "Subject": r["subjects"]["name"],
        "Subject Code": r["subjects"]["subject_code"],
        "is_present": bool(r.get("is_present", False))
    })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count")
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ " + summary["Present_Count"].astype(str) + "/"
        + summary["Total_Count"].astype(str) + " Students"
    )

    display_df = (
        summary.sort_values(by="ts_group", ascending=False)
        [["Time", "Subject Code", "Attendance Stats" ]]
    )
    st.dataframe(display_df, width="stretch" , hide_index =True )



# =========================================================
# TEACHER LOGIN FUNCTION
# =========================================================

def login_teacher(username, password):

    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True

        return True

    return False


# =========================================================
# TEACHER LOGIN SCREEN
# =========================================================

def teacher_screen_login():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    # LEFT SIDE
    with c1:
        header_dashboard()

    # RIGHT SIDE
    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_login_back_btn",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header(
        "Login using password",
        text_alignment="center",
    )

    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter your password",
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    # LOGIN
    with btnc1:
        if st.button(
            "Login",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            key="teacher_login_btn",
        ):
            if login_teacher(
                teacher_username,
                teacher_pass,
            ):
                st.toast("Welcome back!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # REGISTER
    with btnc2:
        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            key="teacher_register_btn",
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


# =========================================================
# REGISTER TEACHER FUNCTION
# =========================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm,
):

    # REQUIRED FIELDS
    if (
        not teacher_username
        or not teacher_name
        or not teacher_pass
        or not teacher_pass_confirm
    ):
        return False, "All fields are required!"

    # USERNAME CHECK
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    # PASSWORD CONFIRMATION
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords don't match"

    # CREATE TEACHER
    try:
        create_teacher(
            teacher_username,
            teacher_pass,
            teacher_name,
        )

        return True, "Successfully created! Login now."

    except Exception as e:
        print("Registration error:", e)
        return False, "Unexpected error!"


# =========================================================
# TEACHER REGISTER SCREEN
# =========================================================

def teacher_screen_register():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    # LEFT SIDE
    with c1:
        header_dashboard()

    # RIGHT SIDE
    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_register_back_btn",
            shortcut="control+backspace",
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    st.header(
        "Register Your Teacher Profile",
        text_alignment="center",
    )

    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
    )

    teacher_name = st.text_input(
        "Enter name",
        placeholder="Ananya Roy",
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter your password",
    )

    teacher_pass_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Confirm your password",
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    # REGISTER
    with btnc1:
        if st.button(
            "Register Now",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            key="teacher_register_now_btn",
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm,
            )

            if success:
                st.success(message)

                import time
                time.sleep(2)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

    # LOGIN
    with btnc2:
        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            key="teacher_login_instead_btn",
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()
