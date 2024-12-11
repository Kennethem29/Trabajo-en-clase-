import tkinter as tk
from tkinter import messagebox

class GestionCalificaciones:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Calificaciones")
        self.alumnos = {}  # Almacena la información de los alumnos por DNI

        # Crear la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Etiquetas y entradas de texto
        tk.Label(self.root, text="DNI:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Apellidos:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Nombre:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Nota:").grid(row=3, column=0, padx=5, pady=5)

        self.dni_entry = tk.Entry(self.root)
        self.apellidos_entry = tk.Entry(self.root)
        self.nombre_entry = tk.Entry(self.root)
        self.nota_entry = tk.Entry(self.root)

        self.dni_entry.grid(row=0, column=1, padx=5, pady=5)
        self.apellidos_entry.grid(row=1, column=1, padx=5, pady=5)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5)
        self.nota_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botones para funcionalidades
        tk.Button(self.root, text="Introducir Alumno", command=self.introducir_alumno).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Mostrar Alumnos", command=self.mostrar_alumnos).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Eliminar Alumno", command=self.eliminar_alumno).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Consultar Alumno", command=self.consultar_alumno).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Modificar Nota", command=self.modificar_nota).grid(row=8, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Mostrar Suspensos", command=self.mostrar_suspensos).grid(row=9, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Mostrar Aprobados", command=self.mostrar_aprobados).grid(row=10, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Candidatos a MH", command=self.mostrar_mh).grid(row=11, column=0, columnspan=2, pady=5)

    def calcular_calificacion(self, nota):
        if nota < 5:
            return "SS"
        elif 5 <= nota < 7:
            return "AP"
        elif 7 <= nota < 9:
            return "NT"
        else:
            return "SB"

    def introducir_alumno(self):
        dni = self.dni_entry.get().strip()
        apellidos = self.apellidos_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        try:
            nota = float(self.nota_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "La nota debe ser un número válido.")
            return

        if dni in self.alumnos:
            messagebox.showerror("Error", "Ya existe un alumno con ese DNI.")
        else:
            calificacion = self.calcular_calificacion(nota)
            self.alumnos[dni] = {"apellidos": apellidos, "nombre": nombre, "nota": nota, "calificacion": calificacion}
            messagebox.showinfo("Éxito", "Alumno introducido correctamente.")

        self.clear_entries()

    def mostrar_alumnos(self):
        if not self.alumnos:
            messagebox.showinfo("Información", "No hay alumnos registrados.")
            return

        alumnos_info = "\n".join(
            [f"{dni} {info['apellidos']}, {info['nombre']} {info['nota']} {info['calificacion']}" for dni, info in self.alumnos.items()]
        )
        messagebox.showinfo("Alumnos", alumnos_info)

    def eliminar_alumno(self):
        dni = self.dni_entry.get().strip()
        if dni in self.alumnos:
            del self.alumnos[dni]
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No existe un alumno con ese DNI.")

        self.clear_entries()

    def consultar_alumno(self):
        dni = self.dni_entry.get().strip()
        if dni in self.alumnos:
            info = self.alumnos[dni]
            messagebox.showinfo("Consulta", f"DNI: {dni}\nApellidos: {info['apellidos']}\nNombre: {info['nombre']}\nNota: {info['nota']}\nCalificación: {info['calificacion']}")
        else:
            messagebox.showerror("Error", "No existe un alumno con ese DNI.")

    def modificar_nota(self):
        dni = self.dni_entry.get().strip()
        try:
            nueva_nota = float(self.nota_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "La nota debe ser un número válido.")
            return

        if dni in self.alumnos:
            self.alumnos[dni]["nota"] = nueva_nota
            self.alumnos[dni]["calificacion"] = self.calcular_calificacion(nueva_nota)
            messagebox.showinfo("Éxito", "Nota modificada correctamente.")
        else:
            messagebox.showerror("Error", "No existe un alumno con ese DNI.")

        self.clear_entries()

    def mostrar_suspensos(self):
        suspensos = [f"{dni} {info['apellidos']}, {info['nombre']} {info['nota']} {info['calificacion']}" for dni, info in self.alumnos.items() if info['nota'] < 5]
        self.mostrar_lista("Suspensos", suspensos)

    def mostrar_aprobados(self):
        aprobados = [f"{dni} {info['apellidos']}, {info['nombre']} {info['nota']} {info['calificacion']}" for dni, info in self.alumnos.items() if info['nota'] >= 5]
        self.mostrar_lista("Aprobados", aprobados)

    def mostrar_mh(self):
        mh = [f"{dni} {info['apellidos']}, {info['nombre']} {info['nota']} {info['calificacion']}" for dni, info in self.alumnos.items() if info['nota'] == 10]
        self.mostrar_lista("Candidatos a MH", mh)

    def mostrar_lista(self, titulo, lista):
        if not lista:
            messagebox.showinfo(titulo, f"No hay {titulo.lower()}.")
        else:
            messagebox.showinfo(titulo, "\n".join(lista))

    def clear_entries(self):
        self.dni_entry.delete(0, tk.END)
        self.apellidos_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.nota_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionCalificaciones(root)
    root.mainloop()
