import re
import tkinter as tk
from tkinter import ttk
import random
import string
from tkinter import messagebox

def password_complexity_checker(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ @!#$%^&*()_+=]", password) is None
    length_bonus = len(password) >= 12
    
    score = 0
    if not length_error:
        score += 1
    if length_bonus:
        score += 1
    if not digit_error:
        score += 1
    if not uppercase_error:
        score += 1
    if not lowercase_error:
        score += 1
    if not symbol_error:
        score += 1

    return {
        'score': score,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }

def get_strength_label(score):
    if score <= 2:
        return "Very Weak"
    elif score == 3:
        return "Weak"
    elif score == 4:
        return "Moderate"
    elif score == 5:
        return "Strong"
    elif score == 6:
        return "Very Strong"

def get_feedback(result):
    feedback = []
    if result['length_error']:
        feedback.append("Password should be at least 8 characters long.")
    if result['digit_error']:
        feedback.append("Password should include at least one digit.")
    if result['uppercase_error']:
        feedback.append("Password should include at least one uppercase letter.")
    if result['lowercase_error']:
        feedback.append("Password should include at least one lowercase letter.")
    if result['symbol_error']:
        feedback.append("Password should include at least one special character (@!#$%^&*()_+=).")
    if not result['length_error'] and len(password_entry.get()) < 12:
        feedback.append("Consider using a longer password (12 or more characters) for extra security.")
    
    return "\n".join(feedback)

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "@!#$%^&*()_+="
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(suggested_password)
    root.update()  # now it stays on the clipboard after the window is closed
    messagebox.showinfo("Copied", "Suggested password copied to clipboard")

def check_password():
    global suggested_password
    password = password_entry.get()
    result = password_complexity_checker(password)
    score = result['score']
    strength = get_strength_label(score)
    feedback = get_feedback(result)
    
    suggestion = ""
    if score < 6:
        suggested_password = generate_strong_password()
        suggestion = f"Suggested Strong Password: {suggested_password}"
        suggested_password_label.config(text=suggestion)
        copy_button.grid(row=4, column=1, sticky="W")
    else:
        suggested_password_label.config(text="")
        copy_button.grid_remove()
    
    result_text = f"Password Strength: {strength}\n\nFeedback:\n{feedback}"
    result_label.config(text=result_text)
    password_entry.delete(0, tk.END)  # Clear password entry

# Setting up the GUI
root = tk.Tk()
root.title("Password Complexity Checker")

style = ttk.Style(root)
style.theme_use('clam')  # Use 'clam' theme for modern look

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

password_label = ttk.Label(frame, text="Enter Password:")
password_label.grid(row=0, column=0, pady=5, sticky=tk.W)

password_entry = ttk.Entry(frame, width=30)
password_entry.grid(row=0, column=1, pady=5, sticky=tk.E)

check_button = ttk.Button(frame, text="Check Password", command=check_password)
check_button.grid(row=1, columnspan=2, pady=10, sticky=(tk.W, tk.E))

result_label = ttk.Label(frame, text="", justify=tk.LEFT, wraplength=400)
result_label.grid(row=2, columnspan=2, pady=10, sticky=(tk.W, tk.E))

suggested_password_label = ttk.Label(frame, text="", justify=tk.LEFT)
suggested_password_label.grid(row=3, column=0, pady=10, sticky=tk.W)

copy_button = ttk.Button(frame, text="📋", command=copy_to_clipboard)
copy_button.grid(row=4, column=1, sticky="W")
copy_button.grid_remove()

# Ensure the frame expands with the window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

root.mainloop()
