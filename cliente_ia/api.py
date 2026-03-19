import requests

BASE_URL = "http://127.0.0.1:8000/api"

def login(username, password):
    return requests.post(f"{BASE_URL}/login/", json={
        "username": username,
        "password": password
    })

def obtener_tareas():
    return requests.get(f"{BASE_URL}/tasks/")