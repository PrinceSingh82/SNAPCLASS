import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(subject):

    # =====================================================
    # GET SUBJECT DETAILS
    # =====================================================

    subject_name = subject.get(
        "name",
        "Unknown Subject"
    )

    subject_code = subject.get(
        "subject_code",
        "N/A"
    )

    # =====================================================
    # JOIN URL
    # =====================================================

    app_domain = "snapclass-main.streamlit.app"

    join_url = f"{app_domain}/?join-code={subject_code}"

    # =====================================================
    # GENERATE QR CODE
    # =====================================================

    qr = segno.make(join_url)

    qr_buffer = io.BytesIO()

    qr.save(
        qr_buffer,
        kind="png",
        scale=8,
        border=2
    )

    qr_bytes = qr_buffer.getvalue()

    # =====================================================
    # CUSTOM DIALOG CSS
    # =====================================================

    st.markdown(
        """
        <style>

        /* ===============================================
           MAIN DIALOG
           =============================================== */

        div[role="dialog"] {

            background-color: #0D1117 !important;

            border-radius: 20px !important;

            box-shadow:
                0 10px 35px
                rgba(0, 0, 0, 0.35) !important;

        }


        /* ===============================================
           DIALOG HEADER
           =============================================== */

        div[role="dialog"]
        [data-testid="stDialogHeader"] {

            background-color: #0D1117 !important;

            border-radius: 20px 20px 0 0 !important;

        }


        /* ===============================================
           SHARE CLASS LINK - WHITE
           =============================================== */

        div[role="dialog"]
        [data-testid="stDialogHeader"] h1,

        div[role="dialog"]
        [data-testid="stDialogHeader"] h2,

        div[role="dialog"]
        [data-testid="stDialogHeader"] h3,

        div[role="dialog"]
        [data-testid="stDialogHeader"] p,

        div[role="dialog"]
        [data-testid="stDialogHeader"] span {

            color: #FFFFFF !important;

            font-family: 'Outfit', sans-serif !important;

            font-weight: 700 !important;

        }


        /* ===============================================
           CLOSE BUTTON
           =============================================== */

        div[role="dialog"]
        [data-testid="stDialogCloseButton"] {

            color: #FFFFFF !important;

        }

        div[role="dialog"]
        [data-testid="stDialogCloseButton"] svg {

            color: #FFFFFF !important;

            fill: #FFFFFF !important;

        }


        /* ===============================================
           DIALOG BODY
           =============================================== */

        div[role="dialog"] > div {

            background-color: #0D1117 !important;

        }


        /* ===============================================
           ALL TEXT
           =============================================== */

        div[role="dialog"] p,
        div[role="dialog"] span,
        div[role="dialog"] label {

            color: #FFFFFF !important;

            font-family: 'Outfit', sans-serif !important;

        }


        /* ===============================================
           HEADINGS
           =============================================== */

        div[role="dialog"] h3,
        div[role="dialog"] h4 {

            color: #FFFFFF !important;

            font-family: 'Outfit', sans-serif !important;

            font-weight: 700 !important;

        }


        /* ===============================================
           CODE BOX
           =============================================== */

        div[role="dialog"]
        [data-testid="stCode"] {

            background-color: #1A1F27 !important;

            border-radius: 9px !important;

            border: none !important;

        }


        /* ===============================================
           CODE TEXT
           =============================================== */

        div[role="dialog"] code {

            background-color: transparent !important;

            color: #FFFFFF !important;

            font-family: 'Outfit', sans-serif !important;

            font-size: 14px !important;

        }


        /* ===============================================
           INFO BOX
           =============================================== */

        div[role="dialog"]
        [data-testid="stAlert"] {

            background-color: #19324A !important;

            border: none !important;

            border-radius: 9px !important;

        }


        div[role="dialog"]
        [data-testid="stAlert"] p {

            color: #42A5F5 !important;

            font-family: 'Outfit', sans-serif !important;

        }


        /* ===============================================
           QR IMAGE
           =============================================== */

        div[role="dialog"] img {

            display: block !important;

            max-width: 100% !important;

            height: auto !important;

            border-radius: 8px !important;

        }


        /* ===============================================
           QR CAPTION
           =============================================== */

        div[role="dialog"]
        [data-testid="stCaptionContainer"] p {

            color: #A9ADB5 !important;

            text-align: center !important;

            font-family: 'Outfit', sans-serif !important;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # SCAN TO JOIN
    # =====================================================

    st.markdown(
        """
        <h3 style="
            color:#FFFFFF !important;
            font-family:'Outfit', sans-serif !important;
            font-weight:700 !important;
            margin-top:5px;
            margin-bottom:20px;
        ">
            Scan to Join
        </h3>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # TWO COLUMNS
    # =====================================================

    col1, col2 = st.columns(
        [1, 1],
        gap="medium"
    )


    # =====================================================
    # LEFT COLUMN
    # =====================================================

    with col1:

        st.markdown(
            """
            <h4 style="
                color:#FFFFFF !important;
                font-family:'Outfit', sans-serif !important;
                font-weight:700 !important;
                margin-bottom:10px;
            ">
                Copy Link
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.code(
            join_url,
            language="text"
        )


        st.markdown(
            """
            <h4 style="
                color:#FFFFFF !important;
                font-family:'Outfit', sans-serif !important;
                font-weight:700 !important;
                margin-top:25px;
                margin-bottom:10px;
            ">
                Subject Code
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.code(
            subject_code,
            language="text"
        )


        st.info(
            "Copy this link or subject code "
            "to share on WhatsApp or Email."
        )


    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with col2:

        st.markdown(
            """
            <h4 style="
                color:#FFFFFF !important;
                font-family:'Outfit', sans-serif !important;
                font-weight:700 !important;
                margin-bottom:10px;
            ">
                Scan to Join
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.image(
            qr_bytes,
            width=240
        )

        st.caption(
            "QR Code for class joining"
        )