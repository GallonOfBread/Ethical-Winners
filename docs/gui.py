import streamlit as st
import email
from email.utils import parseaddr

def load_gui(msgs):
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
