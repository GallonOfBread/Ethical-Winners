import ollama

def analyze_single(msg):
    """Analyzes one email using Llama 3.2 via Ollama."""
    # EXTRACT METADATA
    sender = msg['eml']["From"] or "(unknown sender)"
    subject = msg['eml']["Subject"] or "(no subject)"
    body = (msg['eml'].get_payload() or "").strip()[:2000]
    
    prompt = f"""
    ### SECURITY ANALYSIS TASK ###
    Analyze this email for phishing.
    
    SENDER: {sender}
    SUBJECT: {subject}
    BODY: {body}
    
    INSTRUCTIONS:
    - Determine a Phishing Score (0-100). 
    - Provide a one-sentence Reason.
    - DO NOT provide a breakdown, DO NOT use numbered lists, and DO NOT explain your reasoning beyond the one sentence.
    
    RESPONSE FORMAT:
    Score: [number]
    Reason: [text]
    """

    try:
        response = ollama.chat(model='llama3.2:latest', messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        content = response['message']['content']
        # debug print: print(f"--- DEBUG RAW OUTPUT ---\n{content}\n-----------------------")
        
        score = 0
        reason = "AI analysis complete."

        for line in content.split('\n'):
            clean_line = line.replace('*', '').strip() 
            
            # Looks for line starting with "Score:"
            if clean_line.startswith("Score:"):
                digits = ''.join(filter(str.isdigit, clean_line))
                if digits:
                    score = int(digits)
                    # We found the official score line, stop looking for scores
                    break 
            
        for line in content.split('\n'):
            clean_line = line.replace('*', '').strip() 
            if clean_line.startswith("Reason:"):
                parts = clean_line.split("Reason:", 1)
                if len(parts) > 1:
                    reason = parts[1].strip()
                    break

        return score, reason

    except Exception as e:
        print(f"ERROR: {e}")
        return 0, f"Ollama Error: {str(e)}"

    