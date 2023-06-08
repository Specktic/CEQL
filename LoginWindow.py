from tkinter import *
import os
import xml.etree.ElementTree as ET


class LoginWindow:
    def __init__(self):
        self.login_window = Tk()
        self.login_window.geometry("800x450")
        self.login_window.title("Visualizer")
        self.login_window.config(background="#8e8f99")

        # username text box
        self.username_entry = Entry(
            self.login_window,
            font=("Helvetica", 15)
        )
        self.username_entry.place(x=330, y=150)

        # password text box
        self.password_entry = Entry(
            self.login_window,
            font=("Helvetica", 15),
            show="*"
        )
        self.password_entry.place(x=330, y=200)

        # login button
        self.login_button = Button(
            self.login_window,
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
        self.register_button = Button(
            self.login_window,
            text="Register",
            command=self.register,
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        self.register_button.place(x=420, y=350)

    def login(self):
        if self.username_entry.get() == "test user" and self.password_entry.get() == "test password":
            print("Logged in")
        else:
            print("Username or password doesn't match")
            self.create_register_window()

    def register(self):
        self.create_register_window()

    def create_register_window(self):
        register_window = Tk()
        register_window.geometry("800x450")
        register_window.title("Visualizer")
        register_window.config(background="#8e8f99")

        # name entry
        name_entry = Entry(
            register_window,
            font=("Helvetica", 15)
        )
        name_entry.place(x=330, y=150)

        # attributes entry
        attributes_entry = Entry(
            register_window,
            font=("Helvetica", 15)
        )
        attributes_entry.place(x=330, y=200)

        # register button
        register_button = Button(
            register_window,
            text="Create XML Store",
            command=lambda: self.create_xml(name_entry.get(),attributes_entry.get()),
            font=("Helvetica", 15),
            fg="black",
            bg="white",
            activeforeground="black",
            activebackground="grey",
            state="active"
        )
        register_button.place(x=420, y=350)

        register_window.mainloop()

    def create_xml(self, name,attributes):
        ruta_carpeta_existente = r"C:\Users\micha\OneDrive\Documents\proyecto 3\CEQL\xml"
        ruta_xml_store = os.path.join(ruta_carpeta_existente, name)

        # Verificar si la carpeta ya existe
        if os.path.exists(ruta_xml_store):
            print("La carpeta ya existe:", ruta_xml_store)
        else:
            # Crear la carpeta
            os.makedirs(ruta_xml_store)
            print("Carpeta creada:", ruta_xml_store)
              
            atributos = attributes.split(",")
            print("Atributos:", atributos)

            
            root = ET.Element(name)
            for atributo in atributos:
                elemento = ET.SubElement(root, atributo)

            # Guardar el XML en un archivo dentro de la carpeta
            archivo_xml = os.path.join(ruta_xml_store, f"{name}.xml")
            tree = ET.ElementTree(root)
            tree.write(archivo_xml)

            print("XML creado:", archivo_xml)

    def run(self):
        self.login_window.mainloop()


# Crear instancia de la ventana de inicio de sesión
login = LoginWindow()
# Ejecutar la ventana de inicio de sesión
login.run()


