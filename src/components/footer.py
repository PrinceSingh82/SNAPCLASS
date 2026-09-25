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
            <span>Created with</span>
            <span>by</span>
            <strong>PRINCE SINGH</strong>
            <span style="color: red; font-size: 18px;">❤️</span>
        </div>
        """,
        unsafe_allow_html=True
    )