import streamlit as st
import pandas as pd
import os
import re
import base64


# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="University of Memphis — University Contact Information Form", page_icon="🎓", layout="centered")


st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5 { color: #00498F; font-weight: 700; }
    .stButton > button {
        background-color: #00498F;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:disabled {
        background-color: #999 !important;
        color: #eee !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Background Image Setup
# ----------------------------
background_image = "background.jpg"  # 👈 replace with your image filename

if os.path.exists(background_image):
    with open(background_image, "rb") as f:
        bg_data = base64.b64encode(f.read()).decode()

    # You can adjust the transparency (0.0 = fully transparent, 1.0 = fully opaque)
    opacity = 0.8  # 👈 change this value as needed

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})),
                        url("data:image/jpeg;base64,{bg_data}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Background image not found. Please place 'background.jpg' in this folder.")


# ----------------------------
# Helpers
# ----------------------------
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
def is_email(s: str) -> bool:
    return bool(EMAIL_REGEX.match((s or "").strip()))

# ----------------------------
# Session init
# ----------------------------
if "num_universities" not in st.session_state:
    st.session_state.num_universities = 1


# ----------------------------
# Header Section (Logo + Title side by side)
# ----------------------------
logo_path = "uofm_logo2.png"  # 👈 ensure it's in the same folder

st.markdown(
    """
    <style>
    .header-bar {
        background-color: #00498F;
        color: white;
        font-weight: 800;
        font-size: 1.8rem;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1.5px solid black;
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 1rem;
    }
    .header-text {
        display: flex;
        flex-direction: column;
        justify-content: center;
        line-height: 1.2;
    }
    .header-subtitle {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 3px;
        color: white;
    }
    .header-caption {
        font-size: 0.95rem;
        color: #f0f0f0;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        import base64
        logo_data = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <div class="header-bar">
            <img src="data:image/jpeg;base64,{logo_data}" width="120" style="border-radius:6px;">
            <div class="header-text">
                <div style="font-size:1.8rem; font-weight:800;">University Contact Information Form</div>
                <div class="header-caption">Please complete the details below.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Logo image not found. Please place 'uofm_logo.jpg' in this folder.")

# ----------------------------
# Inputs (LIVE widgets, no st.form)
# ----------------------------
faculty_name = st.text_input("Faculty Name", placeholder="Enter your name")

university_data = []
for i in range(st.session_state.num_universities):
    with st.expander(f"🏫 University {i+1}", expanded=True):
        uni = st.text_input(f"University Name {i+1}", key=f"uni_{i}", placeholder="e.g., University of Memphis").strip()
        contact = st.text_input(f"Contact Name {i+1}", key=f"contact_{i}", placeholder="Enter the contact name").strip()
        desig = st.text_input(f"Designation {i+1}", key=f"desig_{i}", placeholder="e.g., Associate Professor").strip()
        email = st.text_input(f"Email Address {i+1}", key=f"email_{i}", placeholder="example@university.edu").strip()
        university_data.append({
            "University Name": uni,
            "Contact Name": contact,
            "Designation": desig,
            "Email": email
        })

st.markdown("---")
c1, c2 = st.columns([3, 1])
with c1:
    st.caption("Add more university contacts if applicable.")
with c2:
    if st.button("➕ Add university contact"):
        st.session_state.num_universities += 1
        st.rerun()

# ----------------------------
# Enable Submit only when valid
# ----------------------------
# At least one complete university row:
has_complete_row = any(all(v for v in entry.values()) for entry in university_data)

# Optional: basic email check for rows that are complete
if has_complete_row:
    for entry in university_data:
        if all(entry.values()) and not is_email(entry["Email"]):
            has_complete_row = False
            st.warning(f"Invalid email format: {entry['Email']}")
            break

can_submit = bool(faculty_name.strip()) and has_complete_row

st.markdown("---")
submit_clicked = st.button("Submit", disabled=not can_submit)

if not can_submit:
    st.info("ℹ️ Enter **Faculty Name** and complete **all four fields** for at least one university to enable Submit.")

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Save on Submit
# ----------------------------
if submit_clicked:
    valid_entries = [e for e in university_data if all(e.values()) and is_email(e["Email"])]
    if not valid_entries:
        st.warning("Please complete at least one university section with a valid email.")
    else:
        df = pd.DataFrame([{"Faculty Name": faculty_name.strip(), **e} for e in valid_entries])
        csv_path = "submissions.csv"
        if os.path.exists(csv_path):
            old = pd.read_csv(csv_path)
            pd.concat([old, df], ignore_index=True).to_csv(csv_path, index=False)
        else:
            df.to_csv(csv_path, index=False)
        st.success("✅ Form submitted successfully! Your response has been successfully saved.")
# ----------------------------
# Footer
# ----------------------------
footer_opacity = 0.8  # 👈 Change this between 0.0 (fully transparent) and 1.0 (solid blue)

st.markdown(
    f"""
    <style>
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        background-color: rgba(0, 73, 143, {footer_opacity});
        color: white;
        text-align: center;
        padding: 8px 0;
        font-size: 0.9rem;
        font-weight: 600;
        border-top: 1.5px solid black;
        z-index: 100;
        backdrop-filter: blur(4px); /* Optional soft blur for glassy look */
    }}
    </style>

    <div class="footer">
        © The University of Memphis | International Affairs Office
    </div>
    """,
    unsafe_allow_html=True
)