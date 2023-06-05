from tkinter import *


# button functions
def login():
    if username_entry.get() == "test user" and password_entry.get() == "test password":
        print("logged in")
    else:
        print("Username or password doesn't match")


def register():
    print("create new account")


# window attributes
login_window = Tk()
login_window.geometry("800x450")
login_window.title("Visualizer")
login_window.config(background="#8e8f99")

# username text box
username_entry = Entry(
    login_window,
    font=("Helvetica", 15)
)

username_entry.place(x=330, y=150)

# password text box
password_entry = Entry(
    login_window,
    font=("Helvetica", 15)
)

password_entry.place(x=330, y=200)

# login button
login_button = Button(
    login_window,
    text="login",
    command=login,
    font=("Helvetica", 15),
    fg="black",
    bg="white",
    activeforeground="black",
    activebackground="grey",
    state=ACTIVE
)

login_button.place(x=330, y=350)

# register button
register_button = Button(
    login_window,
    text="register",
    command=register,
    font=("Helvetica", 15),
    fg="black",
    bg="white",
    activeforeground="black",
    activebackground="grey",
    state=ACTIVE)

register_button.place(x=420, y=350)

# window loop
login_window.mainloop()
