import streamlit as st
import email
from email.utils import parseaddr
 
msg_strs = [
    '''From: "Jane Smith" <jane.smith@winner.mail>
To: john.johnson@winner.mail
Subject: RE: Curriculum Review
Date: Tue, 01 Apr 2026 09:12:00 -0500
Message-ID: <curriculum.20260401.0912@winner.mail>
Hello John,
Thanks for leading today's curriculum review session — it was really productive!
- Jane Smith''',
    '''From: "Principal Hartley" <d.hartley@winner.mail>
To: john.johnson@winner.mail
Subject: Staff Meeting - Thursday 4PM
Date: Tue, 01 Apr 2026 10:30:00 -0500
Message-ID: <staffmtg.20260401.1030@winner.mail>
Hi John,
Reminder that we have an all-staff meeting this Thursday at 4PM in the library. Please bring your Q3 assessment data.
- Principal Hartley''',
    '''From: "Donna Kowalski" <d.kowalski@winner.mail>
To: john.johnson@winner.mail
Subject: Game Night - Friday Night!
Date: Mon, 31 Mar 2026 18:22:00 -0500
Message-ID: <gamenight.20260331.1822@winner.mail>
John!
Game night is ON for Friday. My place, 7PM. Bring snacks. Kevin says he's "definitely not losing this time" so you know it's going to be a great night.
- Donna'''
]
 
msgs = [email.message_from_string(s) for s in msg_strs]
 
st.set_page_config(page_title="Winner Mail", layout="wide")
 
st.markdown("""
<style>
    /* Sidebar message rows */
    .msg-row {
        padding: 10px 12px;
        border-bottom: 1px solid #2a2a2a;
        cursor: pointer;
        border-radius: 6px;
        margin-bottom: 4px;
        background: #1a1a1a;
        transition: background 0.15s;
    }
    .msg-row:hover { background: #2a2a2a; }
    .msg-row.selected { background: #0d3b66; border-left: 3px solid #4da6ff; }
    .msg-subject { font-weight: 700; font-size: 0.88rem; color: #eee; }
    .msg-sender  { font-size: 0.8rem; color: #aaa; margin-top: 2px; }
 
    /* Reading pane */
    .email-subject { font-size: 1.35rem; font-weight: 700; margin-bottom: 4px; }
    .email-from    { font-size: 0.92rem; color: #555; }
    .email-date    { font-size: 0.85rem; color: #999; margin-bottom: 10px; }
    .email-divider { border: none; border-top: 1px solid #ddd; margin: 10px 0 16px; }
    .email-body    { font-size: 0.95rem; line-height: 1.65; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)
 
# Session state for selected message
if "selected" not in st.session_state:
    st.session_state.selected = 0
 
col_list, col_read = st.columns([1, 2.5])
 
# --- Left panel: message list ---
with col_list:
    st.markdown("### 📬 Inbox")
    for i, msg in enumerate(msgs):
        name, addr = parseaddr(msg["From"])
        display_name = name or addr
        subject = msg["Subject"] or "(no subject)"
        selected_class = "selected" if st.session_state.selected == i else ""
        if st.button(f"**{subject}**\n\n{display_name}", key=f"msg_{i}", use_container_width=True):
            st.session_state.selected = i
 
# --- Right panel: reading pane ---
with col_read:
    idx = st.session_state.selected
    msg = msgs[idx]
    name, addr = parseaddr(msg["From"])
    from_display = f"{name} <{addr}>" if name else addr
    subject = msg["Subject"] or "(no subject)"
    date = msg["Date"] or ""
    body = (msg.get_payload() or "").strip()
 
    st.markdown(f"<div class='email-subject'>{subject}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='email-from'>From: {from_display}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='email-date'>{date}</div>", unsafe_allow_html=True)
    st.markdown("<hr class='email-divider'>", unsafe_allow_html=True)
    st.markdown(f"<div class='email-body'>{body}</div>", unsafe_allow_html=True)
