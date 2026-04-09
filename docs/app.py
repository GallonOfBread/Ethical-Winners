import email, csv, os
import alg, llm, gui

# LOAD DATA ===========================
# Data from:
# https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset
msgs = []

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '250emails.csv'), newline='', mode='r') as file:
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


# LLM ASSESSMENT ===========================
llm.assess(msgs)


# GUI ===========================
gui.load_gui(msgs)
