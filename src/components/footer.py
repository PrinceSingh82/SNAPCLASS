import streamlit as st


def footer_home():

    st.markdown(
        """
        <div style="
            margin-top: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 6px;
            color: white;
            font-family: 'Outfit', sans-serif;
            font-size: 16px;
        ">
            <span>Developed by</span>
            <strong>Prince Singh</strong>
            <span style="color: red; font-size: 18px;">❤️</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def footer_dashboard():

    st.markdown(
        """
        <div style="
            margin-top: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 6px;
            color: black;
            font-family: 'Outfit', sans-serif;
            font-size: 16px;
        ">
            <span>Developed by</span>
            <strong>Prince Singh</strong>
            <span style="color: red; font-size: 18px;">❤️</span>
        </div>
        """,
        unsafe_allow_html=True
    )