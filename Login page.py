import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
from twilio.rest import Client

#  DATABASE SETUP 
conn = sqlite3.connect('users.db')
c = conn.cursor()
conn.commit()

#  GUI SETUP 
root = tk.Tk()
root.title("User Login System with OTP")
root.geometry("400x500")

#  FUNCTIONALITY 
def show_register():
    login_frame.pack_forget()
    register_frame.pack()

def show_login():
    register_frame.pack_forget()
    login_frame.pack()

def register_user():
    name = name_entry.get()
    username = username_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if not (name and username and phone and email):
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    
    try:
        c.execute("INSERT INTO users (username, name, phone, email) VALUES (?, ?, ?, ?)",
                  (username, name, phone, email))
        conn.commit()
        messagebox.showinfo("Success", "Registered successfully!")
        show_login()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

def generate_otp():
    username = login_username_entry.get().strip()

    # Getting phone from database
    c.execute("SELECT phone FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if not result:
        messagebox.showerror("Error", "Username not found.")
        return

    phone = result[0]  # Verified phone number from DB

    TWILIO_SID = 'AC0d497b6210cd2b948bb5c780c2de24f9'
    TWILIO_AUTH = 'e0e68b1c59132e6e4bea367e1939954a'
    TWILIO_PHONE = '+18455991348'

    client = Client(TWILIO_SID, TWILIO_AUTH)

    otp = str(random.randint(100000, 999999))

    # Updating OTP in database
    c.execute("UPDATE users SET otp = ? WHERE username = ?", (otp, username))
    conn.commit()

    try:
        client.messages.create(
            from_=TWILIO_PHONE,
            to=phone,
            body=f"Your OTP is: {otp}"
        )
        messagebox.showinfo("OTP Sent", "OTP has been sent to your registered phone number.")
    except Exception as e:
        messagebox.showerror("Twilio Error", f"Failed to send OTP: {str(e)}")

def verify_otp():
    username = login_username_entry.get()
    user_input = otp_entry.get()

    c.execute("SELECT otp FROM users WHERE username = ?", (username,))
    row = c.fetchone()

    if row and user_input == row[0]:
        messagebox.showinfo("Success", "OTP verification successful!")
    else:
        messagebox.showerror("Failed", "Incorrect OTP. Verification failed.")

#  REGISTER
register_frame = tk.Frame(root)

tk.Label(register_frame, text="Register", font=('Arial', 16)).pack(pady=10)

tk.Label(register_frame, text="Name").pack()
name_entry = tk.Entry(register_frame)
name_entry.pack()

tk.Label(register_frame, text="Username").pack()
username_entry = tk.Entry(register_frame)
username_entry.pack()

tk.Label(register_frame, text="Phone Number").pack()
phone_entry = tk.Entry(register_frame)
phone_entry.pack()

tk.Label(register_frame, text="Email").pack()
email_entry = tk.Entry(register_frame)
email_entry.pack()

tk.Button(register_frame, text="Register", command=register_user).pack(pady=10)
tk.Label(register_frame, text="Already registered?").pack()
tk.Button(register_frame, text="Login", command=show_login, fg="blue", relief=tk.FLAT).pack()

#  LOGIN
login_frame = tk.Frame(root)

tk.Label(login_frame, text="Login", font=('Arial', 16)).pack(pady=10)

tk.Label(login_frame, text="Username").pack()
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack()

tk.Label(login_frame, text="Phone Number").pack()
login_phone_entry = tk.Entry(login_frame)
login_phone_entry.pack()

tk.Button(login_frame, text="Generate OTP", command=generate_otp).pack(pady=5)

tk.Label(login_frame, text="Enter OTP").pack()
otp_entry = tk.Entry(login_frame)
otp_entry.pack()

tk.Button(login_frame, text="Verify OTP", command=verify_otp).pack(pady=5)

tk.Label(login_frame, text="Not registered?").pack()
tk.Button(login_frame, text="Register", command=show_register, fg="blue", relief=tk.FLAT).pack()

# Showing registration page first
register_frame.pack()

root.mainloop()