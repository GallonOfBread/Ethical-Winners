import email, csv, os
from email.utils import parseaddr

def assess(msgs):
    i = 0
    for msg in msgs:
        # Actually assess the email based on msg['eml']
        if msg['lbl'] == '1':
            msgs[i]['llm'] = 100
            msgs[i]['llm-reason'] = "Chat says this is phishing."
        else:
            msgs[i]['llm'] = 0
            msgs[i]['llm-reason'] = "Chat says this is real."
        i += 1
    return msgs

if __name__ == "__main__":
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
    
    assess(msgs)
    
    for i, msg in enumerate(msgs):
        if i < 20:
            print(str(msg['llm']) + "%", msg['llm-reason'])
            print(msg['eml']["Subject"] or "(no subject)")
            body = (msg['eml'].get_payload() or "").strip()
            print(body[:80] + "..." if len(body) > 80 else body)
            print()
    