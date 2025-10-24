import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000"  # URL de tu backend FastAPI


# -------------------------
# Ventana principal: Login
# -------------------------
def mostrar_login():
    root = tk.Tk()
    root.title("Login de Usuario")
    root.geometry("300x300")
    root.configure(bg="lightblue")

    tk.Label(root, text="Email:").pack(pady=5)
    email_entry = tk.Entry(root, width=30)
    email_entry.pack()

    tk.Label(root, text="Contraseña:").pack(pady=5)
    pass_entry = tk.Entry(root, width=30, show="*")
    pass_entry.pack()

    def iniciar_sesion():
        email = email_entry.get().strip()
        password = pass_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Error", "Complete ambos campos.")
            return

        try:
            response = requests.post(f"{API_URL}/SignIn", json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                root.destroy()
                mostrar_lista_usuarios(data["nombre"])
            else:
                messagebox.showerror("Error", response.json().get("detail", "Error de autenticación"))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor login.\n{e}")

    tk.Button(root, text="Ingresar", command=iniciar_sesion).pack(pady=10)
    root.mainloop()


# -------------------------
# Ventana secundaria: Lista de usuarios
# -------------------------
def mostrar_lista_usuarios(nombre_usuario):
    ventana = tk.Tk()
    ventana.title("Usuarios Activos")
    ventana.geometry("500x500")
    ventana.configure(bg="#a1c3ff")

    tk.Label(ventana, text=f"Bienvenido, {nombre_usuario}", font=("Arial", 12, "bold")).pack(pady=10)

    lista = tk.Listbox(ventana, width=50, height=10)
    lista.pack(pady=10)

    def cargar_usuarios():
        try:
            resp = requests.get(f"{API_URL}/Usuarios")
            if resp.status_code == 200:
                usuarios = resp.json()
                lista.delete(0, tk.END)
                for u in usuarios:
                    lista.insert(tk.END, f"{u['nombre']} - {u['email']}")
            else:
                messagebox.showerror("Error", "No se pudieron cargar los usuarios.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor.\n{e}")

    def cerrar_sesion():
        ventana.destroy()
        mostrar_login()

    tk.Button(ventana, text="Actualizar lista", command=cargar_usuarios).pack(pady=5)
    tk.Button(ventana, text="Cerrar sesión", command=cerrar_sesion).pack(pady=5)

    cargar_usuarios()
    ventana.mainloop()


# -------------------------
# Iniciar la app
# -------------------------
if __name__ == "__main__":
    mostrar_login()
