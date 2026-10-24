
import streamlit as st

from src.database.db import create_attendence

def show_attendance_result(df,logs):
        st.write("Please review the attendance before confirming.")
        st.dataframe(df, hide_index=True, width="stretch")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Discard", width="stretch"):
                st.session_state.voice_attendance_results = None
                st.session_state["attendance_images"] = []
                st.rerun()

                st.rerun()

        with col2:
            if st.button(
                "Confirm & Save",
                width="stretch",
                type="primary",
            ):
                try:
                    if not logs:
                        st.warning("No attendance records to save.")
                        return

                    create_attendence(logs)

                    st.toast("Attendance Taken!")

                    # Clear captured photos after successful save
                    st.session_state["attendance_images"] = []
                    st.session_state.voice_attendance_results = None

                    st.rerun()

                except Exception as e:
                    st.error(f"Attendance sync failed: {e}")



@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
     show_attendance_result(df,logs)

