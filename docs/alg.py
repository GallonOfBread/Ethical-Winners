import email, csv, os
from email.utils import parseaddr

import email, csv, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def train_algoritm(dataset_path):
    # This trains a fast statistical model on startup
    texts = []
    labels = []
    
    with open(dataset_path, newline='', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        x = 0
        for row in reader:
            # The for loop skips the first row, which is the column Headers
            if x > 0:
                # Combines subject and body for training
                texts.append(str(row[3]) + " " + str(row[4]))
                # The ground truth label
                labels.append(int(row[5]))
            x += 1
            
    vectorizer = TfidfVectorizer(max_features=3000, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    model = MultinomialNB()
    model.fit(X, labels)
    
    return vectorizer, model

def assess(msgs, vectorizer, model):
    for msg in msgs:
        eml = msg['eml']
        subject = str(eml['Subject']) if eml['Subject'] else ""
        body = str(eml.get_payload())
        combined_text = subject + " " + body
        
        # Transform a single email into a statistical vector
        X_new = vectorizer.transform([combined_text])
        
        # Determine the probability that this email is phishing (Class 1)
        probability = model.predict_proba(X_new)[0][1] 
        
        score = int(probability * 100)
        
        if score > 75:
            reason = "Statistical analysis indicates high similarity to known phishing patterns."
        elif score > 25:
            reason = "Statistical analysis detected ambiguous or risky language patterns."
        else:
            reason = "Few or no statistical anomalies detected."
            
        msg['alg'] = score
        msg['alg-reason'] = reason
        
    return msgs

if __name__ == "__main__":
    # Data from:
    # https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset
    msgs = []

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '2000emails.csv'), newline='', mode='r') as file:
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
            print(str(msg['alg']) + "%", msg['alg-reason'])
            print(msg['eml']["Subject"] or "(no subject)")
            body = (msg['eml'].get_payload() or "").strip()
            print(body[:80] + "..." if len(body) > 80 else body)
            print()