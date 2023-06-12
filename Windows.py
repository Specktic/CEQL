import sqlite3
from tkinter import *
import os
import xml.etree.ElementTree as ET
import Huffman

compressor = Huffman.Compressor()


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
        if self.username_entry.get() == "catconv" and compressor.compress(self.password_entry.get()) == {'i': '00', 'k': '01', 't': '1'}:
            print("Logged in")
            self.database_window()
        else:
            print("Username or password doesn't match")

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
            compressor.compress(pass1)
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

    def create_xml(self, name, attributes):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS xml_documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, xml TEXT)")
        cursor.execute("SELECT id FROM xml_documents WHERE name=?", (name,))
        result = cursor.fetchone()
        if result:
            print("El XML ya existe en la base de datos.")
        else:
            ruta_carpeta_existente = r"CEQL\xml"
            ruta_xml_store = os.path.join(ruta_carpeta_existente, name)
            if not os.path.exists(ruta_xml_store):
                os.makedirs(ruta_xml_store)
                print("Carpeta creada:", ruta_xml_store)
            atributos = attributes.split(",")
            print("Atributos:", atributos)
            root = ET.Element(name)
            for atributo in atributos:
                elemento = ET.SubElement(root, atributo)
            archivo_xml = os.path.join(ruta_xml_store, f"{name}.xml")
            tree = ET.ElementTree(root)
            tree.write(archivo_xml)
            with open(archivo_xml, "r") as f:
                xml_content = f.read()
                cursor.execute("INSERT INTO xml_documents (name, xml) VALUES (?, ?)", (name, xml_content))
                conn.commit()
                print("XML creado y registrado en la base de datos:", archivo_xml)
        conn.close()

    def delete_xml(self, name):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, xml FROM xml_documents WHERE name=?", (name,))
        result = cursor.fetchone()
        if result:
            xml_id, xml_content = result
            cursor.execute("DELETE FROM xml_documents WHERE id=?", (xml_id,))
            conn.commit()
            print("XML eliminado de la base de datos.")
            ruta_carpeta_existente = r"CEQL\xml"
            ruta_xml_store = os.path.join(ruta_carpeta_existente, name)
            archivo_xml = os.path.join(ruta_xml_store, f"{name}.xml")
            if os.path.exists(archivo_xml):
                os.remove(archivo_xml)
                print("Archivo XML eliminado:", archivo_xml)
            if os.path.exists(ruta_xml_store):
                os.rmdir(ruta_xml_store)
                print("Carpeta eliminada:", ruta_xml_store)
        else:
            print("El XML no existe en la base de datos.")
        conn.close()

    def run(self):
        self.welcome_window.mainloop()


# Crea la instancia de la ventana de inicio de sesión
login = Windows()
# Ejecuta la ventana de inicio de sesión
login.run()
