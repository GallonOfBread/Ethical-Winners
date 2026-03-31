import tkinter as tk
import email
from email.utils import parseaddr

msgStrs = [
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

msgs = [email.message_from_string(s) for s in msgStrs]

root = tk.Tk()
root.title("Winner Mail")
root.geometry("800x500")

selected_row = None

# --- left panel ---
left = tk.Frame(root, width=260, bd=1, relief=tk.SUNKEN)
left.pack(side=tk.LEFT, fill=tk.Y)
left.pack_propagate(False)

# --- right panel ---
right = tk.Frame(root)
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

subj_label = tk.Label(right, text="", font=("", 12, "bold"), anchor="w", wraplength=480)
subj_label.pack(fill=tk.X)
from_label = tk.Label(right, text="", anchor="w")
from_label.pack(fill=tk.X)
date_label = tk.Label(right, text="", anchor="w", fg="gray")
date_label.pack(fill=tk.X)
tk.Frame(right, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=6)
body_text = tk.Text(right, wrap=tk.WORD, relief=tk.FLAT, cursor="arrow")
body_text.pack(fill=tk.BOTH, expand=True)
body_text.config(state=tk.DISABLED)

def show_msg(idx):
    global selected_row
    if selected_row is not None:
        selected_row.config(bg="black")
    selected_row = row_frames[idx]
    selected_row.config(bg="lightblue")

    msg = msgs[idx]
    name, addr = parseaddr(msg["From"])
    subj_label.config(text=msg["Subject"] or "(no subject)")
    from_label.config(text=f"{name} <{addr}>" if name else addr)
    date_label.config(text=msg["Date"] or "")
    body_text.config(state=tk.NORMAL)
    body_text.delete("1.0", tk.END)
    body_text.insert("1.0", (msg.get_payload() or "").strip())
    body_text.config(state=tk.DISABLED)

row_frames = []
for i, msg in enumerate(msgs):
    name, addr = parseaddr(msg["From"])
    f = tk.Frame(left, bg="black", cursor="hand2", pady=6, padx=6)
    f.pack(fill=tk.X)
    tk.Label(f, text=msg["Subject"] or "(no subject)", font=("", 9, "bold"), bg="black", anchor="w").pack(fill=tk.X)
    tk.Label(f, text=name or addr, bg="black", anchor="w").pack(fill=tk.X)
    f.bind("<Button-1>", lambda e, idx=i: show_msg(idx))
    for child in f.winfo_children():
        child.bind("<Button-1>", lambda e, idx=i: show_msg(idx))
    row_frames.append(f)

show_msg(0)
root.mainloop()
