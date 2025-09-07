from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """Generate a random password and insert it into the password field."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Randomly choose letters, symbols, and numbers
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)  # shuffle the list to mix letters, symbols, and numbers
    password = "".join(password_list)
    password_entry.insert(0, password)  # inserts generated password into whitespace
    pyperclip.copy(password)  # copies password into clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Save the website, email, and password to a JSON file."""
    website = website_entry.get()
    email = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    # check that fields are not empty
    if len(website) > 0 or len(password) > 0:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)  # clear website field
            password_entry.delete(0, END)  # clear password field
    else:
        messagebox.showinfo(title="Error!", message="Please don't leave any fields empty!")


# ---------------------------- Find Password ------------------------------- #
def find_password():
    """Search for a saved password by website."""
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas for logo
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_txt = Label(text="Website:")
website_txt.grid(row=1, column=0)
UserName_txt = Label(text="Email/Username:")
UserName_txt.grid(row=2, column=0)
password_txt = Label(text="Password:")
password_txt.grid(row=3, column=0)

# Entries
website_entry = Entry(width=32)
website_entry.grid(row=1, column=1)
website_entry.focus()  # Focus cursor on website field
username_entry = Entry(width=51)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, "p.chris331@gmail.com")  # Default email
password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)
pass_gen_button = Button(text="Generate Password", command=generate_password)
pass_gen_button.grid(row=3, column=2)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
