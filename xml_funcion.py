import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from tkinter import ttk
import sqlite3
import os
import shutil


class XMLStoreApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XML Store App")
        self.label_name = tk.Label(self.root, text="Nombre del XML store:")
        self.entry_name = tk.Entry(self.root)
        self.label_attribute_count = tk.Label(self.root, text="Cantidad de atributos:")
        self.entry_attribute_count = tk.Entry(self.root)
        self.create_button = tk.Button(self.root, text="Crear XML", command=self.create_attribute_entries)
        self.commit_button = tk.Button(self.root, text="Commit", command=self.commit_changes)
        self.commit_button.config(state=tk.DISABLED)

        self.label_name.pack()
        self.entry_name.pack()
        self.label_attribute_count.pack()
        self.entry_attribute_count.pack()
        self.create_button.pack()
        self.commit_button.pack()

        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS xml_documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, xml TEXT)")

        self.attribute_entries = []

    def create_attribute_entries(self):
        attribute_count = self.entry_attribute_count.get()

        if not attribute_count.isdigit():
            messagebox.showwarning("Crear XML", "La cantidad de atributos debe ser un número entero.")
            return

        attribute_count = int(attribute_count)

        if attribute_count <= 0:
            messagebox.showwarning("Crear XML", "La cantidad de atributos debe ser mayor a cero.")
            return

        self.clear_attribute_entries()

        for i in range(attribute_count):
            attribute_frame = tk.Frame(self.root)
            attribute_name_label = tk.Label(attribute_frame, text=f"Atributo {i+1} - Nombre:")
            attribute_name_entry = tk.Entry(attribute_frame)
            attribute_name_label.pack(side=tk.LEFT)
            attribute_name_entry.pack(side=tk.LEFT)
            attribute_content_label = tk.Label(attribute_frame, text="Contenido:")
            attribute_content_entry = tk.Entry(attribute_frame)
            attribute_content_label.pack(side=tk.LEFT)
            attribute_content_entry.pack(side=tk.LEFT)
            self.attribute_entries.append((attribute_name_entry, attribute_content_entry))
            attribute_frame.pack()

        self.create_button.config(state=tk.DISABLED)
        self.commit_button.config(state=tk.NORMAL)

    def clear_attribute_entries(self):
        for entry, content_entry in self.attribute_entries:
            entry.destroy()
            content_entry.destroy()
        self.attribute_entries = []

    def create_xml(self):
        name = self.entry_name.get()

        if not name:
            messagebox.showwarning("Crear XML", "El nombre del XML store no puede estar vacío.")
            return

        attribute_count = len(self.attribute_entries)

        if attribute_count == 0:
            messagebox.showwarning("Crear XML", "Debe agregar al menos un atributo.")
            return

        store_dir = os.path.join("xml_stores", name)
        os.makedirs(store_dir, exist_ok=True)

        xml_file = os.path.join(store_dir, f"{name}.xml")
        root = ET.Element(name)

        for entry, content_entry in self.attribute_entries:
            attribute_name = entry.get()

            if not attribute_name:
                messagebox.showwarning("Crear XML", "El nombre del atributo no puede estar vacío.")
                return

            attribute_content = content_entry.get()

            if not attribute_content:
                messagebox.showwarning("Crear XML", "El contenido del atributo no puede estar vacío.")
                return

            attribute_element = ET.SubElement(root, attribute_name)
            attribute_element.text = attribute_content

        tree = ET.ElementTree(root)
        tree.write(xml_file)

        with open(xml_file, "r") as f:
            xml_content = f.read()
            self.cursor.execute("SELECT id FROM xml_documents WHERE name=?", (name,))
            result = self.cursor.fetchone()
            if result:
                messagebox.showinfo("Crear XML", "El XML ya existe en la base de datos.")
            else:
                self.cursor.execute("INSERT INTO xml_documents (name, xml) VALUES (?, ?)", (name, xml_content))
                self.conn.commit()
                messagebox.showinfo("Crear XML", "XML creado y registrado en la base de datos.")

        self.clear_attribute_entries()
        self.entry_name.delete(0, tk.END)
        self.entry_attribute_count.delete(0, tk.END)
        self.create_button.config(state=tk.NORMAL)
        self.commit_button.config(state=tk.NORMAL)

    def commit_changes(self):
        self.create_xml()
        self.conn.commit()
   
        self.root.withdraw()
        xml_app = MainApp()
        xml_app.run()
        self.root.deiconify()

    def run(self):
        self.root.mainloop()

class delete:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XML Store App")
        self.label_name = tk.Label(self.root, text="Nombre del XML store:")
        self.entry_name = tk.Entry(self.root)
        self.commit_button = tk.Button(self.root, text="Commit", command=self.commit_changes)
        self.commit_button.config(state=tk.NORMAL)

        self.entry_name.pack()
        self.commit_button.pack()
    def delete_xml(self, name):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Obtener el nombre base sin el sufijo
        base_name = name
        if "_" in name:
            base_name, _ = name.split("_", 1)
        
        # Eliminar todas las instancias con el nombre base de la base de datos
        cursor.execute("DELETE FROM xml_documents WHERE name LIKE ?", (base_name + "%",))
        conn.commit()
        print("Instancias XML eliminadas de la base de datos.")
        
        # Eliminar los archivos XML en el sistema de archivos
        ruta_carpeta_existente = os.path.abspath("xml_stores")
        ruta_xml_store = os.path.join(ruta_carpeta_existente, base_name)
        
        for file_name in os.listdir(ruta_xml_store):
            if file_name.startswith(base_name) and file_name.endswith(".xml"):
                file_path = os.path.join(ruta_xml_store, file_name)
                os.remove(file_path)
                print("Archivo XML eliminado:", file_path)
        
        # Eliminar el directorio si está vacío
        if not os.listdir(ruta_xml_store):
            os.rmdir(ruta_xml_store)
            print("Carpeta XML eliminada:", ruta_xml_store)

        conn.close()


    def commit_changes(self):
        name = self.entry_name.get()
        if name:
            self.delete_xml(name)
            self.root.withdraw()
            xml_app = MainApp()
            xml_app.run()
            self.root.deiconify()
        else:
            print("Por favor, ingrese un nombre de XML store.")
    def run(self):
        self.root.mainloop()


class insert:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XML Store App")

        # Crear el Treeview
        self.treeview = ttk.Treeview(self.root)
        self.treeview["columns"] = ("ID", "Nombre", "Contenido XML")
        self.treeview.heading("#0", text="Índice")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Contenido XML", text="Contenido XML")
        self.treeview.pack()

        self.label_name = tk.Label(self.root, text="Nombre del XML:")
        self.entry_name = tk.Entry(self.root)
        self.commit_button = tk.Button(self.root, text="Commit", command=self.commit_changes)

        self.label_name.pack()
        self.entry_name.pack()
        self.commit_button.pack()

        self.show_data()



    def insert_xml_instance(self, name):
        # Obtener la ruta del archivo XML original
        ruta_carpeta_existente = os.path.abspath("xml_stores")
        ruta_xml_store = os.path.join(ruta_carpeta_existente, name)
        archivo_xml = os.path.join(ruta_xml_store, name + ".xml")

        if os.path.exists(archivo_xml):
            # Leer el contenido del archivo XML
            with open(archivo_xml, "r") as file:
                content = file.read()

            # Generar un nuevo nombre con sufijo único
            sufijo = 1
            nuevo_nombre = name
            while True:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()

                # Verificar si el nombre ya existe en la base de datos
                cursor.execute("SELECT id, name FROM xml_documents WHERE name=?", (nuevo_nombre,))
                result = cursor.fetchone()
                if result:
                    sufijo += 1
                    nuevo_nombre = f"{name}_{sufijo}"
                else:
                    break

                conn.close()

            # Insertar la instancia en el XML store con el nuevo nombre
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO xml_documents (name, xml) VALUES (?, ?)", (nuevo_nombre, content))
            conn.commit()
            print("Instancia XML insertada en el XML store.")

            # Mostrar los datos insertados
            cursor.execute("SELECT id, name, xml FROM xml_documents WHERE name=?", (nuevo_nombre,))
            result = cursor.fetchone()
            if result:
                xml_id, xml_name, xml_content = result
                print(f"ID: {xml_id}")
                print(f"Nombre: {xml_name}")
                print(f"Contenido XML:\n{xml_content}")
                self.treeview.insert("", "end", text=str(xml_id), values=(xml_id, xml_name, xml_content))
            else:
                print("No se encontraron datos para mostrar.")

            # Crear una copia del archivo XML con el nuevo nombre en la misma carpeta
            nuevo_archivo_xml = os.path.join(ruta_xml_store, nuevo_nombre + ".xml")
            shutil.copyfile(archivo_xml, nuevo_archivo_xml)
            print("Se ha creado una copia del archivo XML con un sufijo único.")

            conn.close()
        else:
            print("El archivo XML no existe:", archivo_xml)


    def commit_changes(self):
        name = self.entry_name.get()

        if name:
            self.insert_xml_instance(name)
            self.entry_name.delete(0, tk.END)
        else:
            print("Por favor, ingrese un nombre.")

    def show_data(self):
        self.treeview.delete(*self.treeview.get_children())

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM xml_documents")
        rows = cursor.fetchall()

        for row in rows:
            xml_id = row[0]
            xml_name = row[1]
            xml_content = row[2]
            self.treeview.insert("", "end", text=str(xml_id), values=(xml_id, xml_name, xml_content))

        conn.close()

    def run(self):
        self.root.mainloop()
class update:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XML Store App")
        self.label_name = tk.Label(self.root, text="Nombre del XML store:")
        self.entry_name = tk.Entry(self.root)
        self.commit_button = tk.Button(self.root, text="actulizar", command=self.commit_changes)
        self.commit_button.config(state=tk.NORMAL)
        self.commit = tk.Button(self.root, text="actulizar Todos", command=self.commits)
        self.commit.config(state=tk.NORMAL)

        self.entry_name.pack()
        self.commit_button.pack()
        self.commit.pack()

    def update_xml_instance(self, name):
        # Verificar si el XML existe en el XML store
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, xml FROM xml_documents WHERE name=?", (name,))
        result = cursor.fetchone()
        
        if result:
            xml_id, xml_name, xml_content = result

            # Mostrar los datos actuales
            print("Datos actuales:")
            print(f"ID: {xml_id}")
            print(f"Nombre: {xml_name}")
            print(f"Contenido XML:\n{xml_content}")

            # Analizar el contenido XML y obtener un diccionario
            xml_dict = self.parse_xml_content(xml_content)

            # Mostrar los campos y solicitar los nuevos valores
            fields = {}
            for field_name, field_value in xml_dict.items():
                new_value = input(f"Ingrese el nuevo valor para '{field_name}' (Valor actual: {field_value}): ")
                fields[field_name] = new_value

            # Actualizar los campos proporcionados
            for field_name, field_value in fields.items():
                xml_dict[field_name] = field_value

            # Generar el contenido XML actualizado
            updated_xml_content = self.generate_xml_content(xml_dict)

            # Actualizar el archivo XML en el sistema de archivos
            xml_folder = os.path.abspath("xml_stores")
            xml_file = os.path.join(xml_folder, name, name + ".xml")

            with open(xml_file, "w") as file:
                file.write(updated_xml_content)

            print("Archivo XML actualizado en el XML store.")

            # Mostrar los datos actualizados
            cursor.execute("SELECT id, name, xml FROM xml_documents WHERE id=?", (xml_id,))
            updated_result = cursor.fetchone()
            if updated_result:
                updated_xml_id, updated_xml_name, updated_xml_content = updated_result
                print("Datos actualizados:")
                print(f"ID: {updated_xml_id}")
                print(f"Nombre: {updated_xml_name}")
                print(f"Contenido XML:\n{updated_xml_content}")
            else:
                print("No se encontraron datos actualizados.")
        else:
            print("El XML no existe en el XML store.")

        conn.close()
    def get_common_xml_dict(self, xml_dicts):
            common_xml_dict = {}
            if xml_dicts:
                common_xml_dict = xml_dicts[0].copy()
                for xml_dict in xml_dicts[1:]:
                    for key, value in common_xml_dict.items():
                        if key not in xml_dict or xml_dict[key] != value:
                            del common_xml_dict[key]
            return common_xml_dict
    def update_xml_instances(self, name):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Obtener todas las instancias del XML con el mismo nombre
        cursor.execute("SELECT id, xml FROM xml_documents WHERE name LIKE ?", (f"{name}_%",))
        results = cursor.fetchall()

        if results:
            # Mostrar los datos actuales
            print("Datos actuales:")
            for xml_id, xml_content in results:
                print(f"ID: {xml_id}")
                print(f"Contenido XML:\n{xml_content}")

            # Analizar el contenido XML y obtener un diccionario común
            xml_dicts = [self.parse_xml_content(xml_content) for _, xml_content in results]
            common_xml_dict = self.get_common_xml_dict(xml_dicts)

            # Mostrar los campos y solicitar el nuevo valor común
            fields = {}
            for field_name, field_value in common_xml_dict.items():
                new_value = input(f"Ingrese el nuevo valor para '{field_name}' (Valor actual: {field_value}): ")
                fields[field_name] = new_value

            # Actualizar los campos proporcionados en todas las instancias
            for xml_id, xml_content in results:
                xml_dict = self.parse_xml_content(xml_content)
                for field_name, field_value in fields.items():
                    xml_dict[field_name] = field_value
                updated_xml_content = self.generate_xml_content(xml_dict)
                cursor.execute("UPDATE xml_documents SET xml=? WHERE id=?", (updated_xml_content, xml_id))

            conn.commit()
            print("Instancias XML actualizadas en el XML store.")

            # Mostrar los datos actualizados
            cursor.execute("SELECT id, xml FROM xml_documents WHERE name LIKE ?", (f"{name}_%",))
            updated_results = cursor.fetchall()
            if updated_results:
                print("Datos actualizados:")
                for xml_id, updated_xml_content in updated_results:
                    print(f"ID: {xml_id}")
                    print(f"Contenido XML:\n{updated_xml_content}")
            else:
                print("No se encontraron datos actualizados.")
        else:
            print("No se encontraron instancias del XML en el XML store.")

        conn.close()
    def commit_changes(self):
        name = self.entry_name.get()

        if name:
            self.update_xml_instance(name)
            self.entry_name.delete(0, tk.END)
            xml_app = MainApp()
            xml_app.run()
            self.root.deiconify()
        else:
            print("Por favor, ingrese un nombre.")
    def commits(self):
        name = self.entry_name.get()

        if name:
            self.update_xml_instances(name)
            self.entry_name.delete(0, tk.END)
            xml_app = MainApp()
            xml_app.run()
            self.root.deiconify()
        else:
            print("Por favor, ingrese un nombre.")
        

    def parse_xml_content(self, xml_content):
        # Analizar el contenido XML y convertirlo en un diccionario
        # Aquí deberías utilizar la biblioteca adecuada para analizar XML, como xml.etree.ElementTree

        # Ejemplo de implementación utilizando xml.etree.ElementTree
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_content)
        xml_dict = {}

        for child in root:
            xml_dict[child.tag] = child.text

        return xml_dict

    def generate_xml_content(self, xml_dict):
        # Generar el contenido XML a partir del diccionario de campos
        # Aquí deberías utilizar la biblioteca adecuada para generar XML, como xml.etree.ElementTree

        # Ejemplo de implementación utilizando xml.etree.ElementTree
        root = ET.Element("root")

        for key, value in xml_dict.items():
            child = ET.Element(key)
            child.text = value
            root.append(child)

        xml_content = ET.tostring(root).decode()

        return xml_content

    def run(self):
        self.root.mainloop()

class Search:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Search XML Instances")

        self.label_num_conditions = tk.Label(self.root, text="Número de condiciones:")
        self.entry_num_conditions = tk.Entry(self.root)
        self.button_create = tk.Button(self.root, text="Crear componentes de búsqueda", command=self.create_search_components)
        self.button_search = tk.Button(self.root, text="Buscar", command=self.search_xml_instances)

        self.label_num_conditions.pack()
        self.entry_num_conditions.pack()
        self.button_create.pack()
        self.button_search.pack()

        self.search_components = []

        self.treeview = ttk.Treeview(self.root)
        self.treeview["columns"] = ("ID", "Nombre", "Contenido XML")
        self.treeview.heading("#0", text="Índice")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Contenido XML", text="Contenido XML")
        self.treeview.pack()

        self.operator = tk.StringVar(value="AND")
        self.radio_and = tk.Radiobutton(self.root, text="AND", variable=self.operator, value="AND")
        self.radio_or = tk.Radiobutton(self.root, text="OR", variable=self.operator, value="OR")
        self.radio_and.pack()
        self.radio_or.pack()

    def create_search_components(self):
        num_conditions = int(self.entry_num_conditions.get())

        # Limpiar componentes anteriores si existen
        self.clear_search_components()

        # Crear nuevos componentes de búsqueda
        for i in range(num_conditions):
            # Crear etiqueta para el campo
            label_field = tk.Label(self.root, text=f"Campo {i+1}:")
            label_field.pack()

            # Crear ComboBox para seleccionar el campo
            combobox_field = ttk.Combobox(self.root, values=["Nombre del Atributo", "Atributo"], state="readonly")
            combobox_field.pack()

            # Crear etiqueta para el valor
            label_value = tk.Label(self.root, text=f"Valor {i+1}:")
            label_value.pack()

            # Crear Entry para ingresar el valor
            entry_value = tk.Entry(self.root)
            entry_value.pack()

            # Agregar los componentes a la lista
            self.search_components.append((combobox_field, entry_value))

        # Ajustar el tamaño de la ventana
        self.root.update()
        self.root.geometry("400x500")

    def clear_search_components(self):
        if self.search_components:
            for component in self.search_components:
                for widget in component:
                    widget.destroy()
            self.search_components = []

    def search_xml_instances(self):
        operator = self.operator.get()

        conditions = []
        for combobox_field, entry_value in self.search_components:
            field = combobox_field.get()
            value = entry_value.get()
            if field and value:
                if field == "Nombre del Atributo":
                    condition = f"xml LIKE '%{value}%'"
                else:
                    condition = f"xml_content LIKE '%{value}%'"
                conditions.append(condition)

        conditions_sql = f" {operator} ".join(conditions)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        query = "SELECT id, xml_name, xml_content FROM xml_documents"
        if conditions:
            query += " WHERE " + conditions_sql

        cursor.execute(query)
        results = cursor.fetchall()

        self.display_results(results)

        conn.close()

    def display_results(self, results):
        self.treeview.delete(*self.treeview.get_children())

        if results:
            for index, result in enumerate(results):
                xml_id, xml_name, xml_content = result
                self.treeview.insert("", "end", text=str(index + 1), values=(xml_id, xml_name, xml_content))
        else:
            print("No se encontraron instancias que cumplan las condiciones.")

    def run(self):
        self.root.mainloop()

    
class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main App")
           # Crear el Treeview
        self.treeview = ttk.Treeview(self.root)
        self.treeview["columns"] = ("ID", "Nombre", "Contenido XML")
        self.treeview.heading("#0", text="Índice")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Contenido XML", text="Contenido XML")
        self.treeview.pack()
        self.label = tk.Label(self.root, text="¡Bienvenido a la aplicación principal!")
        self.button_open = tk.Button(self.root, text="Abrir XML Store App", command=self.open_xml_store_app)
        self.button_update = tk.Button(self.root, text="Actualizar", command=self.update_instances)
        self.button_search = tk.Button(self.root, text="Buscar", command=self.search_instances)
        self.button_delete = tk.Button(self.root, text="Eliminar", command=self.delete_instances)
        self.button_insert = tk.Button(self.root, text="insert", command=self.insert)

        self.label.pack()
        self.button_open.pack()
        self.button_update.pack()
        self.button_search.pack()
        self.button_delete.pack()
        self.button_insert.pack()
        self.show_data()
   
    def open_xml_store_app(self):
       
        self.root.withdraw()
        xml_app = XMLStoreApp()
        xml_app.run()
        self.root.deiconify()

    def delete_instances(self):
        self.root.withdraw()
        xml_app = delete()
        xml_app.run()
        self.root.deiconify()
    def search_instances(self):
        self.root.withdraw()
        xml_app = Search()
        xml_app.run()
        self.root.deiconify()
       
    def update_instances(self):
        
        self.root.withdraw()
        xml_app = update()
        xml_app.run()
        self.root.deiconify()
       
    def insert(self):
        self.root.withdraw()
        xml_app = insert()
        xml_app.run()
        self.root.deiconify()
        
    def show_data(self):
        self.treeview.delete(*self.treeview.get_children())

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM xml_documents")
        rows = cursor.fetchall()

        for row in rows:
            xml_id = row[0]
            xml_name = row[1]
            xml_content = row[2]
            self.treeview.insert("", "end", text=str(xml_id), values=(xml_id, xml_name, xml_content))

        conn.close()
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
