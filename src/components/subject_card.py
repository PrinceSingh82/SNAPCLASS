import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats=None,
    footer_callback=None
):

    html = f"""

<div style="
    background-color: #FFFFFF;
    border: 2px solid #D1D5DB;
    border-left: 8px solid #EB459E;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 6px 18px rgba(30,41,59,0.16);
    color: #1E293B;
">  


    <h3 style="
        margin:0;
        color:#1E293B;
        font-size:1.5rem;
        font-family:'Outfit', sans-serif;
        font-weight:800;
    ">
        {name}
    </h3>


    <div style="
        display:flex;
        gap:10px;
        margin-top:12px;
        flex-wrap:wrap;
    ">

        <span style="
            background:#E0E3FF;
            color:#5865F2;
            padding:6px 12px;
            border-radius:7px;
            font-weight:700;
            font-size:0.9rem;
        ">
            Code: {code}
        </span>


        <span style="
            background:#F1F1F1;
            color:#333333;
            padding:6px 12px;
            border-radius:7px;
            font-weight:600;
            font-size:0.9rem;
        ">
            Section: {section}
        </span>

    </div>
"""

    if stats:

        html += """
    <div style="
        display:flex;
        gap:10px;
        flex-wrap:wrap;
        margin-top:15px;
    ">
"""

        for icon, label, value in stats:

            html += f"""
        <div style="
            background:#F1F5F9;
            padding:8px 14px;
            border-radius:12px;
            font-size:0.9rem;
            color:#25253A;
            border:1px solid #CBD5E1;
        ">
            {icon}
            <b style="color:#111111;">
                {value}
            </b>
            {label}
        </div>
"""

        html += """
    </div>
"""


    html += """
</div>
"""


    # Render HTML
    st.html(html)


    # Footer callback
    if footer_callback:
        footer_callback()