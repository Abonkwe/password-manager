from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import string


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

def generate_password():
    # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
    #            'v',
    #            'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    #            'R',
    #            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letters = string.ascii_letters
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list1 = [random.choice(letters) for char in range(nr_letters)]

    password_list2 = [random.choice(letters) for symbol in range(nr_symbols)]

    password_list3 = [random.choice(numbers) for num in range(nr_numbers)]

    passwords = password_list3 + password_list2 + password_list1
    random.shuffle(passwords)

    user_password = "".join(passwords)
    password_entry.insert(0, user_password)
    pyperclip.copy(user_password)


def find_password():

    search["bg"] = "blue"

    user_website = website_entry.get().lower()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError and json.decoder.JSONDecodeError:
        messagebox.showinfo(title="Not found", message="file not found. Make sure you create the file first")
    else:
        if user_website in data:
            messagebox.showinfo(title="website info",
                                message=f"Email/Username{data[user_website]["email"]}\nPassword: {data[user_website]["password"]}")
        else:
            messagebox.showerror(title="Not found", message="Website info not found")


# ---------------------------- SAVE PASSWORD ------------------------------- #
is_ok = None


def save():
    global is_ok
    user_website = website_entry.get()
    email = username_email_entry.get()
    user_password = password_entry.get()
    new_data = {
        user_website: {
            "email": email,
            "password": user_password,
        }
    }

    if len(user_password) == 0 or len(user_website) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open('data.json', "r") as data_file:
                # Reading the old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                # Saving the updated data
                json.dump(new_data, data_file, indent=2)
        else:
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=2)

                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=50, pady=50, bg="white")
window.title("Password Manager")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
image = PhotoImage(file="logo.png")
password_image = canvas.create_image(100, 99, image=image)
canvas.grid(row=0, column=1)

# labels
website = Label(text="Website:", bg="white", padx=0, pady=0)
website.grid(row=1, column=0)
username_email = Label(text="Email/Username:", bg="white")
username_email.grid(row=2, column=0)
password = Label(text="Password:", bg="white")
password.grid(row=3, column=0)

# Entry boxes
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
username_email_entry = Entry(width=40)
username_email_entry.grid(row=2, column=1, columnspan=2)
username_email_entry.insert(0, "apabookstore@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=37, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search = Button(text="Search", width=14, command=find_password)
search.grid(row=1, column=2)

window.mainloop()
