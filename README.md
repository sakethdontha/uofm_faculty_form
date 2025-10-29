# 🎓 University of Memphis — Faculty Information Form

This Streamlit web application allows faculty contacts from various universities to securely submit different institutional and contact details.  
Each submission is automatically saved to a local CSV file (`submissions.csv`) and an email notification is sent directly to the supervisor at the University of Memphis.

---

## 🧭 Overview

The purpose of this form is to streamline the collection of different university contacts for academic collaborations, exchange programs, and institutional partnerships.

Key features:
- 🧑‍🏫 Faculty Name input (identifies the sender)
- 🏫 Add multiple universities and contact details dynamically
- 📧 Automatic email notification to the supervising professor (Outlook compatible)
- 💾 Local CSV storage for data tracking and record-keeping
- 🎨 University-themed UI with logo, custom background, and modern layout

---

## ⚙️ Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **Backend:** Python (smtplib, email.message, ssl)
- **Data Storage:** CSV (via pandas)
- **Email Delivery:** Outlook SMTP (`smtp.office365.com`)
- **Hosting:** Streamlit Community Cloud

---


