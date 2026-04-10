import streamlit as st
import email, html
import llm
from email.utils import parseaddr

def score_color(score):
    if score is None: return "#555"
    if score <= 25: return "#1a4a1a"    # dark green bg
    if score >= 75: return "#4a1a1a"    # dark red bg
    return "#4a3a00"                    # dark yellow bg

def score_text_color(score):
    if score is None: return "#aaa"
    if score <= 25: return "#6fcf6f"
    if score >= 75: return "#cf6f6f"
    return "#cfb84a"

def load_gui(msgs):
    st.set_page_config(page_title="Winner Mail", layout="wide")

    st.markdown("""
    <style>
        .email-subject { font-size: 1.35rem; font-weight: 700; margin-bottom: 4px; }
        .email-from    { font-size: 0.92rem; color: #888; }
        .email-date    { font-size: 0.85rem; color: #666; margin-bottom: 10px; }
        .email-divider { border: none; border-top: 1px solid #333; margin: 10px 0 16px; }
        .email-body    { font-size: 0.95rem; line-height: 1.65; white-space: pre-wrap; }
        .score-title  { font-size: 0.82rem; color: #ddd; }
        .score-badge   { font-size: 1.25rem; }
        .score-reason  { font-size: 0.82rem; color: #ddd; }
        .score-row     {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 10px;
            width: 48%
        }
    </style>
    """, unsafe_allow_html=True)

    if "selected" not in st.session_state:
        st.session_state.selected = 0

    col_list, col_read = st.columns([1, 2.5])

    # --- Left panel: scrollable message list ---
    with col_list:
        st.markdown("### 📬 Inbox")
        with st.container(height=700):
            for i, msg in enumerate(msgs):
                name, addr = parseaddr(msg['eml']["From"])
                display_name = name or addr
                subject = msg['eml']["Subject"] or "(no subject)"
                if st.button(f"**{subject}**\n\n{display_name}", key=f"msg_{i}", use_container_width=True):
                    st.session_state.selected = i

    # --- Right panel: reading pane ---
    with col_read:
        idx = st.session_state.selected
        msg = msgs[idx]
        name, addr = parseaddr(msg['eml']["From"])
        from_display = f"{name} &lt;{addr}&gt;" if name else addr
        subject  = html.escape(msg['eml']["Subject"] or "(no subject)")
        date     = html.escape(msg['eml']["Date"] or "")
        body     = html.escape((msg['eml'].get_payload() or "").strip())

        alg_score = msg.get('alg')
        llm_score = msg.get('llm')

        st.markdown(f"<div class='email-subject'>{subject}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='email-from'>From: {from_display}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='email-date'>{date}</div>", unsafe_allow_html=True)
        st.markdown("<hr class='email-divider'>", unsafe_allow_html=True)
        # Score badges - build both in one markdown call
        scores_html = "<div style='display:flex; gap:12px; margin-bottom:10px;'>"
        for label, score, reason_key in [("Algorithmic", alg_score, 'alg-reason'), ("LLM", llm_score, 'llm-reason')]:
            bg     = score_color(score)
            fg     = score_text_color(score)
            pct    = f"{score}%" if score is not None else "—"
            reason = html.escape(str(msg.get(reason_key, "")))
            scores_html += f"""
                <div class='score-row' style='background:{bg}; color:{fg};'>
                    <div class='score-title'>{label}</div>
                    <span class='score-badge'>{pct}</span>
                    <span class='score-reason'>{reason}</span>
                </div>"""
        scores_html += "</div>"
        st.markdown(scores_html, unsafe_allow_html=True)

        st.markdown("<hr class='email-divider'>", unsafe_allow_html=True)

        # AI scan button
        if st.button("🔍 Scan with Llama 3.2", use_container_width=True):
            with st.spinner("Ollama is analyzing the message..."):
                # This calls the single-assessment function we'll add to llm.py
                score, reason = llm.analyze_single(msg)
                msg['llm'] = score
                msg['llm-reason'] = reason
                st.rerun()
        #####

        # Scrollable body
        with st.container(height=500):
            st.markdown(f"<div class='email-body'>{body}</div>", unsafe_allow_html=True)