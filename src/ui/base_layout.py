import streamlit as st


# =========================================================
# HOME BACKGROUND
# =========================================================

def style_background_home():

    st.markdown(
        """
        <style>

            .stApp {
                background-color: #5865F2 !important;
            }

            [data-testid="stAppViewContainer"] {
                background-color: #5865F2 !important;
            }

            [data-testid="stHeader"] {
                background-color: transparent !important;
            }

            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 25px !important;
            }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD BACKGROUND
# =========================================================

def style_background_dashboard():

    st.markdown(
        """
        <style>

            /* Dashboard Background */

            .stApp {
                background-color: #C9CCFF !important;
            }

            [data-testid="stAppViewContainer"] {
                background-color: #C9CCFF !important;
            }

            section[data-testid="stMain"] {
                background-color: #C9CCFF !important;
            }

            [data-testid="stHeader"] {
                background-color: transparent !important;
            }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BASE LAYOUT
# =========================================================

def style_base_layout():

    st.markdown(
        """
        <style>

            /* =================================================
               GOOGLE FONTS
               ================================================= */

            @import url(
                'https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap'
            );


            /* =================================================
               HIDE STREAMLIT DEFAULT UI
               ================================================= */

            #MainMenu,
            footer,
            header {
                visibility: hidden;
            }


            /* =================================================
               MAIN CONTAINER
               ================================================= */

            .block-container {
                padding-top: 1.5rem !important;
            }


            /* =================================================
               H1
               ================================================= */

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: white !important;
            }


            /* =================================================
               DASHBOARD SNAP CLASS TITLE
               ================================================= */

            .dashboard-title {
                color: #5865F2 !important;
                font-family: 'Climate Crisis', sans-serif !important;
                margin: 0 !important;
            }


            /* =================================================
               WELCOME TEXT
               ================================================= */

            .stApp h3 {
                color: black !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
            }

            .stApp h4 {
                color: black !important;
                font-family: 'Outfit', sans-serif !important;
            }


            /* =================================================
               H2
               ================================================= */

            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
                color: black !important;
            }


            /* =================================================
               LOGIN LABELS
               ================================================= */

            [data-testid="stWidgetLabel"] p {
                color: black !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
            }


            /* =================================================
               INPUT BOX
               ================================================= */

            [data-testid="stTextInput"] input {
                background-color: white !important;
                color: black !important;
                border: 1px solid #cccccc !important;
                border-radius: 8px !important;
            }

            [data-testid="stTextInput"] input::placeholder {
                color: black !important;
                opacity: 1 !important;
            }


            /* =================================================
               SUBJECT CARD
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] {

                background: #FFFFFF !important;
                background-color: #FFFFFF !important;

                border: 2px solid #C8C8C8 !important;

                border-radius: 20px !important;

                padding: 20px !important;

                box-shadow:
                    0 7px 18px
                    rgba(0, 0, 0, 0.08) !important;

                color: #25253A !important;
            }


            /* =================================================
               CARD INNER AREA
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] > div,
            div[data-testid="stVerticalBlockBorderWrapper"] > div > div,
            div[data-testid="stVerticalBlockBorderWrapper"] > div > div > div {

                background: #FFFFFF !important;
                background-color: #FFFFFF !important;

                border-radius: 18px !important;
            }


            /* =================================================
               CARD TEXT
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] p,
            div[data-testid="stVerticalBlockBorderWrapper"] span,
            div[data-testid="stVerticalBlockBorderWrapper"] label {

                color: #25253A !important;

                font-family: 'Outfit', sans-serif !important;
            }


            /* =================================================
               CARD HEADINGS
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] h3,
            div[data-testid="stVerticalBlockBorderWrapper"] h4 {

                color: #111111 !important;

                font-family: 'Outfit', sans-serif !important;

                font-weight: 800 !important;
            }


            /* =================================================
               STRONG TEXT
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] strong {

                color: #25253A !important;
            }


            /* =================================================
               CODE BADGE
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] code {

                background-color: #E5E3FF !important;

                color: #5865F2 !important;

                padding: 4px 8px !important;

                border-radius: 6px !important;

                font-weight: 700 !important;
            }


            /* =================================================
               METRIC LABEL
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stMetricLabel"] {

                color: #4A4960 !important;

                font-family: 'Outfit', sans-serif !important;

                font-weight: 600 !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stMetricLabel"] p,

            div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stMetricLabel"] span {

                color: #4A4960 !important;
            }


            /* =================================================
               METRIC VALUE
               ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stMetricValue"] {

                color: #111111 !important;

                font-family: 'Outfit', sans-serif !important;

                font-weight: 800 !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stMetricValue"] div,

            div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stMetricValue"] p {

                color: #111111 !important;
            }


            /* =================================================
               SECONDARY BUTTON
               ================================================= */

            button[kind="secondary"] {

                border-radius: 1.5rem !important;

                background: #EB459E !important;

                color: white !important;

                padding: 10px 20px !important;

                border: none !important;

                transition:
                    transform 0.25s ease-in-out,
                    box-shadow 0.25s ease-in-out !important;
            }

            button[kind="secondary"] p {

                color: white !important;

                font-family: 'Outfit', sans-serif !important;

                font-weight: 600 !important;
            }


            /* =================================================
               TERTIARY BUTTON
               ================================================= */

            button[kind="tertiary"] {

                border-radius: 1.5rem !important;

                background: black !important;

                color: white !important;

                padding: 10px 20px !important;

                border: none !important;

                transition:
                    transform 0.25s ease-in-out,
                    box-shadow 0.25s ease-in-out !important;
            }

            button[kind="tertiary"] p {

                color: white !important;

                font-family: 'Outfit', sans-serif !important;

                font-weight: 600 !important;
            }


            /* =================================================
               PRIMARY BUTTON
               ================================================= */

            button[kind="primary"] {

                border-radius: 1.5rem !important;

                background: #5865F2 !important;

                color: white !important;

                border: none !important;
            }

            button[kind="primary"] p {

                color: white !important;

                font-family: 'Outfit', sans-serif !important;

                font-weight: 600 !important;
            }


            /* =================================================
               BUTTON HOVER
               ================================================= */

            button[kind="secondary"]:hover,
            button[kind="tertiary"]:hover,
            button[kind="primary"]:hover {

                transform: scale(1.05);
            }

        </style>
        """,
        unsafe_allow_html=True
    )