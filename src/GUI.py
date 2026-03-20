from src.constants import DB_USAGE_TYPE_ENUMS
from src.Neo4jInteraction import Neo4jInteraction
from src.RedisInteraction import RedisInteraction
from PIL import ImageTk, Image
from ttkbootstrap.widgets.scrolled import ScrolledText
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import tkinter as tk
import os
from dotenv import load_dotenv
load_dotenv()


# use both db types as a default
DB_USAGE_TYPE = int(os.getenv('DB_USAGE_TYPE', DB_USAGE_TYPE_ENUMS.both))
print(DB_USAGE_TYPE)

redis = RedisInteraction()
neo = Neo4jInteraction()

root = ttk.Window(themename="cyborg")
root.title("HelioNet DB")
root.geometry("1300x1024")
style = ttk.Style()


# background image set up
bg_image = Image.open("bg.png").resize((1920, 1085))
tk_bg_image = ImageTk.PhotoImage(bg_image)
bg_label = ttk.Label(root, image=tk_bg_image)
bg_label.place(x=0, y=0)


# creating functionality elements
def close_GUI():
    print("I am closing, no terminal hanging")
    root.destroy()


def get_all_diseases():
    match(DB_USAGE_TYPE):
        case DB_USAGE_TYPE_ENUMS.neo:
            data = neo.get_all_diseases()
        case _:
            data = redis.get_all_diseases()
    if isinstance(data[0], dict):
        data = [dat.get('id') for dat in data]
    return data


def get_disease_id():
    user_input = entry1.get()
    if user_input:
        match(DB_USAGE_TYPE):
            case DB_USAGE_TYPE_ENUMS.neo:
                print("usingneo")
                data = neo.get_disease_by_id(user_input)
            case _:
                print("usingred")
                data = redis.get_disease_by_id(user_input)

    else:
        print("I didn't get that, can please you enter the disease ID again?")
    print("gotdata", data)
    report = (f"DISEASE: {data['name']}\n"
              f"DRUGS: {', '.join(data['drugs'])}\n"
              f"LOCATIONS: {', '.join(data['locations'])}\n"
              f"GENES: {', '.join(data['genes'])}")

    result_label.text.delete('1.0', END)
    result_label.text.insert(END, f"Results:\n {report}")
    result_label.pack(fill=BOTH, expand=YES, padx=20, pady=20)


def clear_results():
    result_label.text.delete('1.0', END)
    result_label.pack_forget()


def get_compounds():
    user_input = entry1.get()
    output_text = 'Empty'
    if user_input:
        match(DB_USAGE_TYPE):
            case DB_USAGE_TYPE_ENUMS.redis:
                compound_list = redis.get_disease_drug_interactions_by_id(
                    user_input)
            case _:
                compound_list = neo.get_disease_drug_interactions_by_id(
                    user_input)
        if not compound_list:
            output_text = "Ups! No compounds on sight"
        else:
            output_text = f"Here is the compunds list:\n {compound_list}"
    else:
        output_text = "I didn't get that, can you please enter the disease ID again?"

    # print(compound_list)

    result_label.text.delete('1.0', END)
    result_label.text.insert(END, output_text)
    result_label.pack(fill=BOTH, expand=YES, padx=20, pady=20)


# display settings

# making font bigger
style.configure("success.TButton", font=("Times New Roman", 20))
style.configure("info.TButton", font=("Times New Roman", 20))

# some guidance for the user
label1 = ttk.Label(root, text="Welcome! You only have two choices",
                   bootstyle="success", font=("Times New Roman", 24))
label1.pack(padx=20, pady=40)

# display


# space for user input
disease_id_lb = ttk.Label(
    root, text="Enter you disease id:", font=("Times New Roman", 24))
disease_id_lb.pack(padx=5, pady=10)
# entry1 = ttk.Entry(root,  bootstyle="secondary")
options=get_all_diseases()
# dropdown for diseases
entry1 = ttk.Combobox(root, font=("Times New Roman", 24), values=options, bootstyle="info")
entry1.pack(pady=10)
entry1.set("DOID:0050742")

# find elements related to diseases
button1 = ttk.Button(root, text="Let's find your disease associates!",
                     style="success.TButton", command=get_disease_id)
button1.pack(padx=5, pady=10)


# find new compounds button
button2 = ttk.Button(root, text="Let's find compounds!",
                     style="info.TButton", command=get_compounds)
button2.pack(padx=5, pady=10)



# space for results
result_label = ScrolledText(
    root, height=10, autohide=True, font=("Times New Roman", 15))

# clear results
clear_result = ttk.Button(root, text="Clear Results",
                          bootstyle="Danger", command=clear_results)
clear_result.pack(padx=5, pady=10)

# exit button
importantbutton = ttk.Button(
    root, text="Exit", bootstyle="Danger", command=close_GUI)
importantbutton.pack(side="bottom", padx=5, pady=10)

if __name__ == "__main__":
    root.mainloop()
