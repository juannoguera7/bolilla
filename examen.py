import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import sqlite3
import random

# Conexión a la base de datos
conn = sqlite3.connect('preguntas.db')
cursor = conn.cursor()

# Creación de tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    contraseña TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS preguntas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pregunta TEXT NOT NULL,
                    correcta TEXT NOT NULL,
                    incorrecta1 TEXT NOT NULL,
                    incorrecta2 TEXT NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id))''')

conn.commit()

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Preguntas")
        
        # Tamaño de la ventana en píxeles (249.3 mm × 164.3 mm a aproximadamente 96 DPI)
        width = int(249.3 * 3.7795275591)  # 1 mm = 3.7795275591 píxeles
        height = int(164.3 * 3.7795275591)
        
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)  # No redimensionable pero sí minimizable
        self.root.configure(bg='#0A7DAF')  # Color de fondo

        self.usuario_id = None

        # Creación de marcos
        self.marco_login = tk.Frame(root, padx=10, pady=10, bg='#0A7DAF')
        self.marco_registro = tk.Frame(root, padx=10, pady=10, bg='#0A7DAF')
        self.marco_preguntas = tk.Frame(root, padx=10, pady=10, bg='#0A7DAF')
        self.marco_juego = tk.Frame(root, padx=10, pady=10, bg='#0A7DAF')

        # Configuración de widgets en el marco de login
        self.configurar_login()

        # Configuración de widgets en el marco de registro
        self.configurar_registro()

        # Configuración de widgets en el marco de preguntas
        self.configurar_preguntas()

        # Configuración de widgets en el marco del juego
        self.configurar_juego()

        # Mostrar marco de login inicialmente
        self.mostrar_login()

    def configurar_login(self):
        tk.Label(self.marco_login, text="Usuario", bg='#0A7DAF', fg='white').grid(row=0, column=0, padx=5, pady=5)
        self.ingresar_usuario = tk.Entry(self.marco_login)
        self.ingresar_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.marco_login, text="Contraseña", bg='#0A7DAF', fg='white').grid(row=1, column=0, padx=5, pady=5)
        self.ingresar_contraseña = tk.Entry(self.marco_login, show='*')
        self.ingresar_contraseña.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.marco_login, text="Iniciar Sesión", command=self.login_usuario, bg='#D8A700').grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        tk.Button(self.marco_login, text="Registrar", command=self.mostrar_registro, bg='#D8A700').grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def configurar_registro(self):
        tk.Label(self.marco_registro, text="Nuevo Usuario", bg='#0A7DAF', fg='white').grid(row=0, column=0, padx=5, pady=5)
        self.nuevo_usuario = tk.Entry(self.marco_registro)
        self.nuevo_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.marco_registro, text="Nueva Contraseña", bg='#0A7DAF', fg='white').grid(row=1, column=0, padx=5, pady=5)
        self.nueva_contraseña = tk.Entry(self.marco_registro, show='*')
        self.nueva_contraseña.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.marco_registro, text="Guardar", command=self.registrar_usuario, bg='#D8A700').grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        tk.Button(self.marco_registro, text="Volver", command=self.mostrar_login, bg='#D8A700').grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def configurar_preguntas(self):
        tk.Label(self.marco_preguntas, text="Pregunta", bg='#0A7DAF', fg='white').grid(row=0, column=0, padx=5, pady=5)
        self.ingresar_pregunta = tk.Entry(self.marco_preguntas)
        self.ingresar_pregunta.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.marco_preguntas, text="Respuesta Correcta", bg='#0A7DAF', fg='white').grid(row=1, column=0, padx=5, pady=5)
        self.ingresar_correcta = tk.Entry(self.marco_preguntas)
        self.ingresar_correcta.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.marco_preguntas, text="Respuesta Incorrecta 1", bg='#0A7DAF', fg='white').grid(row=2, column=0, padx=5, pady=5)
        self.ingresar_incorrecta1 = tk.Entry(self.marco_preguntas)
        self.ingresar_incorrecta1.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.marco_preguntas, text="Respuesta Incorrecta 2", bg='#0A7DAF', fg='white').grid(row=3, column=0, padx=5, pady=5)
        self.ingresar_incorrecta2 = tk.Entry(self.marco_preguntas)
        self.ingresar_incorrecta2.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.marco_preguntas, text="Añadir Pregunta", command=self.agregar_preguntas, bg='#D8A700').grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Botón Empezar el Juego en marco_preguntas
        tk.Button(self.marco_preguntas, text="Empezar el Juego", command=self.mostrar_juego, bg='#D8A700').grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Botón Regresar en marco_preguntas, debajo del botón Empezar el Juego
        tk.Button(self.marco_preguntas, text="Regresar", command=self.mostrar_login, bg='#D8A700').grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def configurar_juego(self):
        self.label_preguntas = tk.Label(self.marco_juego, text="", bg='#0A7DAF', fg='white')
        self.label_preguntas.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.button_option1 = tk.Button(self.marco_juego, text="", bg='#D8A700', anchor='w')
        self.button_option1.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.button_option2 = tk.Button(self.marco_juego, text="", bg='#D8A700', anchor='w')
        self.button_option2.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.button_option3 = tk.Button(self.marco_juego, text="", bg='#D8A700', anchor='w')
        self.button_option3.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.contador_correcto = tk.IntVar()
        self.contador_incorrecto = tk.IntVar()

        # Tamaño de letra aumentado y configuración de colores
        font_config = tkfont.Font(size=14, weight='bold')

        self.label_correct = tk.Label(self.marco_juego, text="Correctas: 0", fg="white", bg='#2D9231', font=font_config)
        self.label_correct.grid(row=4, column=0, padx=5, pady=5, sticky='w')

        self.label_incorrect = tk.Label(self.marco_juego, text="Incorrectas: 0", fg="white", bg='#D8232A', font=font_config)
        self.label_incorrect.grid(row=4, column=1, padx=5, pady=5, sticky='e')

        # Botón Regresar en marco_juego
        tk.Button(self.marco_juego, text="Regresar", command=self.mostrar_preguntas, bg='#D8A700').grid(row=5, column=1, padx=5, pady=5, sticky='se')

    def mostrar_login(self):
        self.ocultar_todos_marcos()
        self.marco_login.place(relx=0.5, rely=0.5, anchor='center')

    def mostrar_registro(self):
        self.ocultar_todos_marcos()
        self.marco_registro.place(relx=0.5, rely=0.5, anchor='center')

    def mostrar_preguntas(self):
        self.ocultar_todos_marcos()
        self.marco_preguntas.place(relx=0.5, rely=0.5, anchor='center')

    def mostrar_juego(self):
        self.ocultar_todos_marcos()
        self.marco_juego.place(relx=0.5, rely=0.5, anchor='center')
        self.iniciar_preguntas()

    def ocultar_todos_marcos(self):
        self.marco_login.place_forget()
        self.marco_registro.place_forget()
        self.marco_preguntas.place_forget()
        self.marco_juego.place_forget()

    def registrar_usuario(self):
        usuario = self.nuevo_usuario.get()
        contraseña = self.nueva_contraseña.get()

        if usuario and contraseña:
            try:
                cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña))
                conn.commit()
                
                messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
                self.mostrar_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El nombre de usuario ya existe.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def login_usuario(self):
        usuario = self.ingresar_usuario.get()
        contraseña = self.ingresar_contraseña.get()

        cursor.execute("SELECT id FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
        usuarioss = cursor.fetchone()

        if usuarioss:
            self.usuario_id = usuarioss[0]
            messagebox.showinfo("Login", "Inicio de sesión exitoso.")
            self.mostrar_preguntas()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def agregar_preguntas(self):
        pregunta = self.ingresar_pregunta.get()
        correcta = self.ingresar_correcta.get()
        incorrecta1 = self.ingresar_incorrecta1.get()
        incorrecta2 = self.ingresar_incorrecta2.get()

        if pregunta and correcta and incorrecta1 and incorrecta2:
            cursor.execute("INSERT INTO preguntas (pregunta, correcta, incorrecta1, incorrecta2, usuario_id) VALUES (?, ?, ?, ?, ?)",
                           (pregunta, correcta, incorrecta1, incorrecta2, self.usuario_id))
            conn.commit()
            messagebox.showinfo("Pregunta", "Pregunta añadida exitosamente.")
            self.ingresar_pregunta.delete(0, tk.END)
            self.ingresar_correcta.delete(0, tk.END)
            self.ingresar_incorrecta1.delete(0, tk.END)
            self.ingresar_incorrecta2.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def iniciar_preguntas(self):
        cursor.execute("SELECT * FROM preguntas WHERE usuario_id = ?", (self.usuario_id,))
        preguntass = cursor.fetchall()

        if not preguntass:
            messagebox.showerror("Error", "No hay preguntas en el banco de datos.")
            return

        self.pregunta_actual = random.choice(preguntass)
        options = [self.pregunta_actual[2], self.pregunta_actual[3], self.pregunta_actual[4]]
        random.shuffle(options)

        self.label_preguntas.config(text=self.pregunta_actual[1])
        self.button_option1.config(text=options[0], command=lambda: self.check_pregunta(self.pregunta_actual[2], options[0]))
        self.button_option2.config(text=options[1], command=lambda: self.check_pregunta(self.pregunta_actual[2], options[1]))
        self.button_option3.config(text=options[2], command=lambda: self.check_pregunta(self.pregunta_actual[2], options[2]))

    def check_pregunta(self, pregunta_correcta, pregunta_seleccionada):
        if pregunta_correcta == pregunta_seleccionada:
            self.contador_correcto.set(self.contador_correcto.get() + 1)
            self.label_correct.config(text=f"Correctas: {self.contador_correcto.get()}")
            messagebox.showinfo("Respuesta", "¡Correcto!")
        else:
            self.contador_incorrecto.set(self.contador_incorrecto.get() + 1)
            self.label_incorrect.config(text=f"Incorrectas: {self.contador_incorrecto.get()}")
            messagebox.showerror("Respuesta", f"Incorrecto. La respuesta correcta era: {pregunta_correcta}")

        self.iniciar_preguntas()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
