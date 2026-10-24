
import streamlit as st
from PIL import Image



@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write("Add classroom photos to scan for attendance")

    # Initialize session state
    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    t1, t2 = st.columns(2)

    with t1:
        type_camera = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "secondary"
        )

        if st.button(
            "Camera",
            type=type_camera,
            width="stretch",
        ):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:
        type_upload = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "secondary"
        )

        if st.button(
            "Upload photos",
            type=type_upload,
            width="stretch",
        ):
            st.session_state.photo_tab = "upload"
            st.rerun()

    # Camera tab
    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input(
            "Take Snapshot",
            key="dialog_cam",
        )

        if cam_photo:
            image = Image.open(cam_photo).copy()
            st.session_state.attendance_images.append(image)
            st.toast("Photo captured successfully!")

    # Upload tab
    elif st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload",
        )

        if uploaded_files:
            for file in uploaded_files:
                # Avoid adding the same upload repeatedly
                if file.name not in st.session_state.get(
                    "uploaded_photo_names", []
                ):
                    image = Image.open(file).copy()
                    st.session_state.attendance_images.append(image)

                    if "uploaded_photo_names" not in st.session_state:
                        st.session_state.uploaded_photo_names = []

                    st.session_state.uploaded_photo_names.append(file.name)

            st.success("Uploaded photos added successfully!")

    # Preview and finish
    st.divider()

    st.write(
        f"Photos selected: {len(st.session_state.attendance_images)}"
    )

    if st.session_state.attendance_images:
        preview_cols = st.columns(3)

        for index, image in enumerate(
            st.session_state.attendance_images
        ):
            with preview_cols[index % 3]:
                st.image(
                    image,
                    caption=f"Photo {index + 1}",
                    width="stretch",
                )

    if st.button(
        "Done",
        type="primary",
        width="stretch",
    ):
        st.rerun()
