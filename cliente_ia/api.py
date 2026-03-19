import requests

BASE_URL = "http://127.0.1:8000/api/"

#CREATE
def crear_tarea(titulo, descripcion):
    response = requests.post( f"{BASE_URL}/task/create/",
        json={"titulo": titulo, "descripcion": descripcion})
    return response.json()

#READ
def listar_tareas():
    response = requests.get(f"{BASE_URL}/task/")
    return response.json()

#UPDATE
def actualizar_tarea(task_id, titulo, descripcion):
    response = requests.get(f"{BASE_URL}/task/{task_id}/update/",
        json={"titulo": titulo, "descripcion": descripcion})
    return response.json()

#DELETE

def eliminar_tarea(task_id):
    response = requests.delete(f"{BASE_URL}/task/{task_id}/delete/")
    return response.json()
