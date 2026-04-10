import email, csv, os
import streamlit as st
import alg, gui

# LOAD DATA ===========================
# Data from:
# https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

# Check if we already have the emails in memory to prevent resetting on every button click
if 'msgs' not in st.session_state:
    msgs = []

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '250emails.csv'), newline='', mode='r', encoding='utf-8') as file:
        # DictReader automatically uses the first row as headers
        reader = csv.reader(file)

        # Access data
        x = 0
        for row in reader:
            if 1 < x:
                msgs.append({'eml':email.message_from_string(f'''From: {row[0]}
To: {row[1]}
Subject: {row[3]}
Date: {row[2]}
{row[4]}'''
                ),'lbl':row[5]})
            x += 1

    # ALGORITHMIC ASSESSMENT ===========================
    alg.assess(msgs)
    
    # Save the list so it persists during the LLM scan reruns
    st.session_state.msgs = msgs

# Tell the app to always work with the saved version of the list
msgs = st.session_state.msgs

# LLM ASSESSMENT ===========================
# llm.assess(msgs) # removed, we will analyze messages one at a time


# GUI ===========================
gui.load_gui(msgs)
