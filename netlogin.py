import tkinter as tk
import customtkinter as ctk
import requests
import datetime
import time

ctk.set_appearance_mode("system")

root = ctk.CTk()
root.geometry("240x260")
root.resizable(0,0)
root.title("IU Network")


def show_login_frame():
    login_frame.pack(fill="both", padx=10, pady=10, expand=True)
    logout_frame.pack_forget()

def show_logout_frame():
    login_frame.pack_forget()
    logout_frame.pack(fill="both", padx=10, pady=10, expand=True)


def login(username, password, a):
    chk = 0
    try:
        r = requests.get("http://192.168.8.1:8090")
        chk = r.status_code
    except:
        if chk != 200:
            login_status_label.configure(text="Network Not Connected", text_color="red")
    if (chk == 200):
        payload = {"mode" :"191", "username" : username, "password": password, "a": a, "producttype": "0" }
        r = requests.post("http://192.168.8.1:8090/login.xml",payload)
        data = str(r.content)
        if "You are signed in as" in data:
            show_logout_frame()
        elif "Invalid user name/password" in data:
            login_status_label.configure(text="Invalid username or password", text_color="red")
        elif "maximum login limit" in data:
            login_status_label.configure(text="Max limit reached", text_color="red")


def logout(username, password, a):
    payload = {"mode" :"193", "username" : username, "password": password, "a": a, "producttype": "0" }
    r = requests.post("http://192.168.8.1:8090/logout.xml",payload)
    show_login_frame()
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    login_status_label.configure(text="")
    root.focus()



date_time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
a = str(time.mktime(date_time.timetuple()))

# Adding login frame widgets
login_frame = ctk.CTkFrame(root)
login_frame.pack(fill="both", padx=10, pady=10, expand=True)

login_text = ctk.CTkLabel(login_frame, text="Internet Login", font=ctk.CTkFont(size=20, family="Roboto"))
login_text.pack(pady=20)

username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", border_width=0)
username_entry.pack(pady=(10,5), fill='x', padx=20)

password_entry = ctk.CTkEntry(login_frame, show="*", placeholder_text="Password", border_width=0)
password_entry.pack(pady=(10,5), fill='x', padx=20)

login_status_label = ctk.CTkLabel(login_frame, text="")
login_status_label.pack()

login_button = ctk.CTkButton(login_frame, text="Login", command=lambda: login(username_entry.get(),password_entry.get(),a))
login_button.pack(pady=5, fill='x', padx=20)


# Adding logout frame widgets
logout_frame = ctk.CTkFrame(root)

logout_status_label = ctk.CTkLabel(logout_frame, text="Successfully logged in!", font=ctk.CTkFont(size=15, family="Roboto"))
logout_status_label.pack(pady=(5,0),padx=10, anchor="center", expand=True)

logout_button = ctk.CTkButton(logout_frame, text="Logout", command=lambda: logout(username_entry.get(),password_entry.get(),a))
logout_button.pack(anchor="center", expand=True)

show_login_frame()

root.mainloop()