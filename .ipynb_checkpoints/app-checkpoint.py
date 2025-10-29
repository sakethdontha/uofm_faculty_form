import re
import os
import smtplib
import ssl
from email.message import EmailMessage

import streamlit as st

# ----------------------------
# App Config & Theme
# ----------------------------
st.set_page_config(page_title="University of Memphis • Faculty Form", page_icon="🎓", layout="centered")

UOFM_BLUE = "#003087"
UOFM_GOLD = "#FFD200"
UOFM_LIGHT = "#F6F8FA"

st.markdown(f"""
<style>
/* page background */
.reportview-container .main .block-container{{
  padding-top:1.5rem;
  padding-bottom:2rem;
}}

.main {{
  background: white;
}}

/* title styling */
h1, h2, h3 {{
  color: {UOFM_BLUE};
  font-weight: 700;
  letter-spacing: .2px;
}}

/* form card */
.form-card {{
  background: {UOFM_LIGHT};
  border: 1px solid #E5E7EB;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 14px rgba(0,0,0,0.04);
}}

/* submit button */
div.stButton > button:first-child {{
  background-color: {UOFM_BLUE};
  color: white;
  border-radius: 12px;
  padding: 0.6rem 1.1rem;
  border: none;
  font-weight: 600;
}}
div.stButton > button:first-child:hover {{
  background-color: #022a6a;
}}

/* success/warn styling tweaks */
.stAlert > div {{
  border-radius: 12px;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Secrets (set later in Streamlit Cloud; local fallback via env for testing)
# ----------------------------
EMAIL_ADDRESS = st.secrets.get("EMAIL_ADDRESS", os.getenv("EMAIL_ADDRESS", ""))
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", os.getenv("EMAIL_PASSWORD", ""))
PROFESSOR_EMAIL = st.secrets.get("PROFESSOR_EMAIL", os.getenv("PROFESSOR_EMAIL", "professor@memphis.edu"))

# ----------------------------
# Header / Branding
# ----------------------------
col_logo, col_title = st.columns([1, 3])
with col_logo:
    st.image("uofm_logo.png", width=140)
with col_title:
    st.markdown(f"<h2>University of Memphis — Faculty Information Form</h2>", unsafe_allow_html=True)
    st.write("Please complete the details below. On submit, a notification is emailed to the professor.")

st.markdown("---")

# ----------------------------
# Helper: email validation
# ----------------------------
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_email(s: str) -> bool:
    return bool(EMAIL_REGEX.match(s or ""))

# ----------------------------
# Email sending (HTML)
# ----------------------------
def send_html_email(to_addr: str, subject: str, html_body: str, text_fallback: str = ""):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_addr
    if text_fallback.strip() == "":
        text_fallback = "A new faculty form has been submitted."
    msg.set_content(text_fallback)
    msg.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# ----------------------------
# Form UI
# ----------------------------
st.markdown('<div class="form-card">', unsafe_allow_html=True)
with st.form("faculty_form", clear_on_submit=False):
    faculty_name = st.text_input("Faculty Name (who received this form)", placeholder="Enter your name")
    university_name = st.text_input("University Name", placeholder="e.g., University of Texas")
    contact_name = st.text_input("Contact Name", placeholder="Enter contact person’s name")
    designation = st.text_input("Designation", placeholder="e.g., Associate Professor")
    email = st.text_input("Email Address", placeholder="example@university.edu")

    submitted = st.form_submit_button("Submit")

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Submit handling
# ----------------------------
if submitted:
    # Basic validations
    missing = [lbl for lbl, val in [
        ("Faculty Name", faculty_name),
        ("University Name", university_name),
        ("Contact Name", contact_name),
        ("Designation", designation),
        ("Email Address", email),
    ] if not val]

    if missing:
        st.warning(f"Please fill all fields: {', '.join(missing)}.")
    elif not is_email(email):
        st.warning("Please enter a valid Email Address.")
    elif not (EMAIL_ADDRESS and EMAIL_PASSWORD and PROFESSOR_EMAIL):
        st.error("Email credentials are not configured. Add EMAIL_ADDRESS, EMAIL_PASSWORD, and PROFESSOR_EMAIL to Streamlit secrets.")
    else:
        # Build a clean HTML email
        html = f"""
        <div style="font-family: Arial, sans-serif; line-height:1.5;">
          <h2 style="color:{UOFM_BLUE}; margin-bottom:0.4rem;">New Faculty Form Submission</h2>
          <p style="margin-top:0;">The following details were submitted via the University of Memphis faculty form:</p>
          <table cellpadding="8" cellspacing="0" style="border-collapse:collapse; background:#fafafa;">
            <tr><td><b>Faculty Name</b></td><td>{faculty_name}</td></tr>
            <tr><td><b>University</b></td><td>{university_name}</td></tr>
            <tr><td><b>Contact Name</b></td><td>{contact_name}</td></tr>
            <tr><td><b>Designation</b></td><td>{designation}</td></tr>
            <tr><td><b>Email</b></td><td>{email}</td></tr>
          </table>
          <p style="font-size:12px;color:#555;margin-top:1rem;">This is an automated notification from the UofM Faculty Information Form.</p>
        </div>
        """
        text = (
            "New Faculty Form Submission\n\n"
            f"Faculty Name: {faculty_name}\n"
            f"University: {university_name}\n"
            f"Contact Name: {contact_name}\n"
            f"Designation: {designation}\n"
            f"Email: {email}\n"
        )

        try:
            send_html_email(
                to_addr=PROFESSOR_EMAIL,
                subject=f"[UofM] Faculty Form Submission — {faculty_name}",
                html_body=html,
                text_fallback=text
            )
            st.success("✅ Form submitted. The professor has been notified via email.")
        except Exception as e:
            st.error(f"❌ Could not send email: {e}")
