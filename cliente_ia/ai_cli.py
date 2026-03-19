import requests
import getpass

# CONFIGURACIÓN
BASE_URL = "http://127.0.0.1:8000/api"

def login_usuario():
    print("=== LOGIN ===")
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    try:
        response = requests.post(f"{BASE_URL}/login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            print(" Login exitoso")
            return True
        else:
            print(" Error:", response.json())
            return False

    except Exception as e:
        print(" Error de conexión:", e)
        return False

# CREAR TAREA
def crear_tarea():
    print("\n--- Crear Tarea ---")
    titulo = input("Título: ")
    descripcion = input("Descripción: ")

    data = {
        "title": titulo,
        "description": descripcion,
        "status": "Pendiente"
    }

    response = requests.post(f"{BASE_URL}/tasks/create/", json=data)
    print("Respuesta:", response.json())

# VER TAREAS
def ver_tareas():
    print("\n--- Lista de Tareas ---")
    response = requests.get(f"{BASE_URL}/tasks/")
    print(response.json())


# ACTUALIZAR TAREA
def actualizar_tarea():
    print("\n--- Actualizar Tarea ---")
    task_id = input("ID de la tarea: ")
    estado = input("Nuevo estado (Pendiente / En progreso / Completada): ")

    data = {
        "status": estado
    }

    response = requests.put(f"{BASE_URL}/tasks/{task_id}/update/", json=data)
    print("Respuesta:", response.json())


# ELIMINAR TAREA
def eliminar_tarea():
    print("\n--- Eliminar Tarea ---")
    task_id = input("ID de la tarea: ")

    response = requests.delete(f"{BASE_URL}/tasks/{task_id}/delete/")
    print("Respuesta:", response.json())





def procesar_comando(texto):
    texto = texto.lower()

    if "crear" in texto:
        return "crear"

    elif "ver" in texto or "listar" in texto:
        return "ver"

    elif "completar" in texto or "actualizar" in texto:
        return "actualizar"

    elif "eliminar" in texto or "borrar" in texto:
        return "eliminar"

    else:
        return "desconocido"





def main():

    if not login_usuario():
        return

    print("\n IA: Hola, puedo ayudarte con tus tareas")
    print("Escribe: crear, ver, actualizar, eliminar o salir\n")

    while True:
        user_input = input("Tú: ")

        if user_input.lower() == "salir":
            print(" Hasta luego")
            break

        accion = procesar_comando(user_input)

        if accion == "crear":
            crear_tarea()

        elif accion == "ver":
            ver_tareas()

        elif accion == "actualizar":
            actualizar_tarea()

        elif accion == "eliminar":
            eliminar_tarea()

        else:
            print(" IA: No entendí, intenta con: crear, ver, actualizar o eliminar")




if __name__ == "__main__":
    main()