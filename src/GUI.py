import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from RedisInteraction import RedisInteraction

root = ttk.Window(themename = "cyborg")
root.title("HelioNet DB")
root.geometry("800x600")
style = ttk.Style()

def close_GUI():
    print("I am closing, no terminal hanging")
    root.destroy()

def get_disease_id():
    user_input = entry1.get()
    if user_input.empty():
        print("I didn't get that, can please you enter the disease ID again?")
    else:
        get_disease_by_id(user_input)
        
# making font bigger
style.configure("success.TButton",font=("Times New Roman", 20))
style.configure("info.TButton",font=("Times New Roman", 20))

# some guidance for the user
label1 = ttk.Label(root, text = "Welcome! You only have two choices", bootstyle="succes", font = ("Times New Roman", 24))
label1.pack(padx=20, pady=40)



button1 = ttk.Button(root, text="Let's find your disease associates!" ,  style="success.TButton", command=get_disease_id)
button1.pack(padx=5, pady=10)

# space for user input
entry1 = ttk.Entry(root,  style="success.TButton")
entry1.pack( pady=10)


button2 = ttk.Button(root, text="Let's find compounds!" ,style="info.TButton")
button2.pack(padx=5, pady=10)

importantbutton = ttk.Button(root, text="Exit", bootstyle = "Danger", command=close_GUI)
importantbutton.pack(side="bottom",padx=5, pady=10)

root.mainloop()

