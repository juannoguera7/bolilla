 Documentación del Código

Este código implementa una aplicación de preguntas utilizando `tkinter` para la interfaz gráfica y `sqlite3` para la base de datos. A continuación se detalla cada sección del código.

 1. Conexión y Creación de la Base de Datos

```python
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
```
Se conecta a una base de datos SQLite llamada `preguntas.db`. Si las tablas `usuarios` y `preguntas` no existen, se crean. La tabla `usuarios` almacena los usuarios y sus contraseñas, y la tabla `preguntas` almacena las preguntas junto con sus respuestas y el ID del usuario que las creó.

 2. Clase Aplicacion

La clase `Aplicacion` gestiona toda la lógica de la interfaz gráfica y la interacción con la base de datos.

```python
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
```
El constructor de la clase inicializa la ventana principal y sus marcos (`login`, `registro`, `preguntas` y `juego`), configurando cada uno de ellos.

 3. Configuración de los Marcos

Cada marco se configura mediante métodos específicos:

```python
def configurar_login(self):
    tk.Label(self.marco_login, text="Usuario", bg='#0A7DAF', fg='white').grid(row=0, column=0, padx=5, pady=5)
    self.ingresar_usuario = tk.Entry(self.marco_login)
    self.ingresar_usuario.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(self.marco_login, text="Contraseña", bg='#0A7DAF', fg='white').grid(row=1, column=0, padx=5, pady=5)
    self.ingresar_contraseña = tk.Entry(self.marco_login, show='*')
    self.ingresar_contraseña.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(self.marco_login, text="Iniciar Sesión", command=self.login_usuario, bg='#D8A700').grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
    tk.Button(self.marco_login, text="Registrar", command=self.mostrar_registro, bg='#D8A700').grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
```
El método `configurar_login` establece los widgets necesarios para la interfaz de inicio de sesión. De manera similar se configuran los demás marcos (`registro`, `preguntas`, `juego`).

 4. Métodos para Mostrar Marcos

```python
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
```
Estos métodos permiten cambiar entre los diferentes marcos de la interfaz.

 5. Métodos de Usuario y Preguntas

```python
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

    if pregunta y correcta y incorrecta1 y incorrecta2:
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
```
Estos métodos permiten registrar usuarios, iniciar sesión y agregar preguntas a la base de datos.

 6. Lógica del Juego

```python
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
        self.contador_correcto.set(self

.contador_correcto.get() + 1)
    else:
        self.contador_incorrecto.set(self.contador_incorrecto.get() + 1)

    self.iniciar_preguntas()
```
Estos métodos manejan la lógica del juego, seleccionando preguntas aleatorias y verificando las respuestas del usuario.

 7. Widgets del Juego

```python
self.label_preguntas = tk.Label(self.marco_juego, text="", wraplength=300, bg='#0A7DAF', fg='white')
self.label_preguntas.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

self.button_option1 = tk.Button(self.marco_juego, text="", wraplength=200, bg='#D8A700')
self.button_option1.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

self.button_option2 = tk.Button(self.marco_juego, text="", wraplength=200, bg='#D8A700')
self.button_option2.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

self.button_option3 = tk.Button(self.marco_juego, text="", wraplength=200, bg='#D8A700')
self.button_option3.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
```
Los botones y etiquetas se configuran para mostrar las preguntas y opciones de respuesta.

 8. Iniciar la Aplicación

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

    conn.close()
```
Finalmente, se inicia la aplicación y se cierra la conexión a la base de datos al salir.

Este código proporciona una aplicación básica de preguntas con funcionalidades de registro, inicio de sesión, adición de preguntas y un modo de juego que presenta preguntas aleatorias al usuario.
