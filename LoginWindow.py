import shutil
import sqlite3
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
        self.login_window.destroy()
        

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
        delete_button = Button(
            register_window,
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

        register_window.mainloop()

    def create_xml(self,name, attributes):
    
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

       
        cursor.execute("CREATE TABLE IF NOT EXISTS xml_documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, xml TEXT)")

        
        cursor.execute("SELECT id FROM xml_documents WHERE name=?", (name,))
        result = cursor.fetchone()

        if result:
            print("El XML ya existe en la base de datos.")
        else:
          
            ruta_carpeta_existente = r"C:\Users\micha\OneDrive\Documents\proyecto 3\CEQL\xml"
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
    def delete_xml(self,name):
      
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        
        cursor.execute("SELECT id, xml FROM xml_documents WHERE name=?", (name,))
        result = cursor.fetchone()

        if result:
        
            xml_id, xml_content = result
            cursor.execute("DELETE FROM xml_documents WHERE id=?", (xml_id,))
            conn.commit()
            print("XML eliminado de la base de datos.")

            ruta_carpeta_existente = r"C:\Users\micha\OneDrive\Documents\proyecto 3\CEQL\xml"
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
        self.login_window.mainloop()


# Crear instancia de la ventana de inicio de sesión
login = LoginWindow()
# Ejecutar la ventana de inicio de sesión
login.run()


