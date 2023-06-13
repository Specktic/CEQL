import sqlite3
import csv
import serial.tools.list_ports
from tkinter import *
import os
import xml.etree.ElementTree as ET
import Huffman
import UserManagement

compressor = Huffman.Compressor()
users = UserManagement.UserManager()

# Serial communication
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []


class Windows:
    def __init__(self):
        self.welcome_window = Tk()
        self.welcome_window.geometry("800x450")
        self.welcome_window.title("Welcome")
        self.welcome_window.config(background="#8e8f99")

        # username label
        self.username_label = Label(
            self.welcome_window,
            text="Username",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        self.username_label.place(x=220, y=150)

        # username text box
        self.username_entry = Entry(
            self.welcome_window,
            font=("Helvetica", 15)
        )
        self.username_entry.place(x=330, y=150)

        # password label
        self.password_label = Label(
            self.welcome_window,
            text="Password",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        self.password_label.place(x=220, y=200)

        # password text box
        self.password_entry = Entry(
            self.welcome_window,
            font=("Helvetica", 15),
            show="*"
        )
        self.password_entry.place(x=330, y=200)

        # login button
        self.login_button = Button(
            self.welcome_window,
            text="Login",
            command=self.login,
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        self.login_button.place(x=330, y=350)

        # register button
        self.register_account_button = Button(
            self.welcome_window,
            text="Register",
            command=self.register,
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        self.register_account_button.place(x=420, y=350)

    def login(self):
        user = self.username_entry.get()
        password = compressor.compress(self.password_entry.get())
        if users.login(user, password):
            self.database_window()
        else:
            print("nu uh")

    def register(self):
        self.registration_window()

    # Opens account registration window
    def registration_window(self):
        registration_window = Tk()
        registration_window.geometry("800x450")
        registration_window.title("Register Account")
        registration_window.config(background="#8e8f99")
        self.welcome_window.destroy()

        # new account username label
        new_username_label = Label(
            registration_window,
            text="Username",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        new_username_label.place(x=238, y=100)

        # new account username text box
        new_username_entry = Entry(
            registration_window,
            font=("Helvetica", 15)
        )
        new_username_entry.place(x=360, y=100)

        # new account name label
        new_name_label = Label(
            registration_window,
            text="Name",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        new_name_label.place(x=273, y=150)

        # new account name entry
        new_name_entry = Entry(
            registration_window,
            font=("Helvetica", 15)
        )
        new_name_entry.place(x=360, y=150)

        # new account password label
        new_password_label = Label(
            registration_window,
            text="Password",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        new_password_label.place(x=236, y=200)

        # new account password entry
        new_password_entry = Entry(
            registration_window,
            font=("Helvetica", 15)
        )
        new_password_entry.place(x=360, y=200)

        # new account confirm password label
        new_password_confirmation_label = Label(
            registration_window,
            text="Confirm your password",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        new_password_confirmation_label.place(x=120, y=250)

        # new account confirm password entry
        new_password_confirmation_entry = Entry(
            registration_window,
            font=("Helvetica", 15)
        )
        new_password_confirmation_entry.place(x=360, y=250)

        # Create account button
        new_account_button = Button(
            registration_window,
            text="Create Account",
            command=lambda: self.new_account(
                new_name_entry.get(),
                new_username_entry.get(),
                new_password_entry.get(),
                new_password_confirmation_entry.get()
            ),
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        new_account_button.place(x=360, y=300)

    @staticmethod
    def new_account(name, username, pass1, pass2):
        if name != '' and username != '' and pass1 != '' and pass2 != '' and pass1 == pass2:
            f = open("Accounts.csv", "a", newline="")
            newAcc = []
            newAcc.append(name)
            newAcc.append(username)
            newAcc.append(compressor.compress(pass1))
            writer = csv.writer(f)
            writer.writerow(newAcc)
            f.close()

        else:
            print("nuh uh")

    # Opens main database window when logged in
    def database_window(self):
        database_window = Tk()
        database_window.geometry("800x450")
        database_window.title("Visualizer")
        database_window.config(background="#8e8f99")
        self.welcome_window.destroy()

        # name label
        name_label = Label(
            database_window,
            text="XML name",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        name_label.place(x=190, y=150)

        # name entry
        name_entry = Entry(
            database_window,
            font=("Helvetica", 15)
        )
        name_entry.place(x=330, y=150)

        # attributes label
        attributes_label = Label(
            database_window,
            text="XML attributes",
            font=("Helvetica", 15),
            fg="black",
            bg="#8e8f99"
        )
        attributes_label.place(x=190, y=200)

        # attributes entry
        attributes_entry = Entry(
            database_window,
            font=("Helvetica", 15)
        )
        attributes_entry.place(x=330, y=200)

        # register button
        create_file_button = Button(
            database_window,
            text="Create XML Store",
            command=lambda: self.create_xml(name_entry.get(), attributes_entry.get()),
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        create_file_button.place(x=420, y=350)
        delete_button = Button(
            database_window,
            text="delete",
            command=lambda: self.delete_xml(name_entry.get()),
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        delete_button.place(x=300, y=350)
        database_window.mainloop()




    def run(self):
        self.welcome_window.mainloop()

        serialInst.baudrate = 9600
        serialInst.port = "COM3"
        serialInst.open()
        while True:
            if serialInst.in_waiting:
                pack = serialInst.readline()
                print(pack.decode('utf'))
            else:
                break


# Crea la instancia de la ventana de inicio de sesión
login = Windows()
# Ejecuta la ventana de inicio de sesión
login.run()
