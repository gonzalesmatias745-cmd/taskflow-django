from api import login, obtener_tareas
from cliente_ia.ai_cli import preguntar
import getpass

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

res = login(username, password)

if res.status_code == 200:
    print("Login OK")

    while True:
        msg = input("Tú: ")

        if msg == "salir":
            break

        if "tareas" in msg:
            tareas = obtener_tareas().json()
            print("Tareas:", tareas)
        else:
            print("IA:", preguntar(msg))
else:
    print("Error login")