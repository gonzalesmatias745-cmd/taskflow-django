from .firebase_config import db
import uuid
from datetime import datetime


def registrar_usuario(data):
    user_id = str(uuid.uuid4())

    user = {
        "user_id": user_id,
        "username": data["username"],
        "email": data["email"],
        "password": data["password"],  # TODO: Hash password in production
        "created_at": datetime.now(),
    }

    db.collection("usuarios").document(user_id).set(user)

    return user


def iniciar_sesion(email, password):
    users = db.collection("usuarios").stream()

    for doc in users:
        user_data = doc.to_dict()

        if user_data["email"] == email and user_data["password"] == password:
            return {
                "message": "Inicio de sesión exitoso",
                "user" : user_data
            }
    
    return {"error": "Credenciales inválidas"}


def create_task(data):
    task_id = str(uuid.uuid4())

    task = {
        "task_id": task_id,
        "title": data["title"],
        "description": data["description"],
        "assigned_to": data.get("assigned_to", ""),
        "status": data.get("status", "pendiente"),
        "priority": data.get("priority", "media"),
        "due_date": data.get("due_date", ""),
        "created_at": datetime.now(),
    }

    db.collection("tareas").document(task_id).set(task)

    return task


def get_tasks():
    tasks = []

    docs = db.collection("tareas").stream()

    for doc in docs: 
        task = doc.to_dict()
        task["id"] = doc.id
        tasks.append(task)

    return tasks


def update_task_status(task_id, status):
    task_ref = db.collection("tareas").document(task_id)

    task_ref.update({
        "status": status
    })

    return {"message": "Estado de la tarea actualizado correctamente"}


def delete_task(task_id):
    db.collection("tareas").document(task_id).delete()

    return {"message": "Tarea eliminada correctamente"}
