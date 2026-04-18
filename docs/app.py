import email, csv, os
import streamlit as st
import alg, gui

# LOAD DATA ===========================
# Data from:
# https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

# Check if we already have the emails in memory to prevent resetting on every button click
if 'msgs' not in st.session_state:
    msgs = []

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '2000emails.csv'), newline='', mode='r', encoding='utf-8') as file:
        # DictReader automatically uses the first row as headers
        reader = csv.reader(file)

        # Access data
        x = 0
        for row in reader:
            if 0 < x:
                msgs.append({'eml':email.message_from_string(f'''From: {row[0]}
To: {row[1]}
Subject: {row[3]}
Date: {row[2]}
{row[4]}'''
                ),'lbl':row[5]})
            x += 1

    # ALGORITHMIC ASSESSMENT ===========================
    # Define the path to the dataset
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '2000emails.csv')
    
    # Train the statistical model (happens instantly)
    vectorizer, model = alg.train_algoritm(dataset_path)
    
    # Calls the assess function of alg.py with the messages, vectorizer, and model as parameters
    alg.assess(msgs, vectorizer, model)
    
    # Save the list so it persists during the LLM scan reruns
    st.session_state.msgs = msgs

# Tell the app to always work with the saved version of the list
msgs = st.session_state.msgs

# LLM ASSESSMENT ===========================
# llm.assess(msgs) # removed, we will analyze messages one at a time


# GUI ===========================
gui.load_gui(msgs)
