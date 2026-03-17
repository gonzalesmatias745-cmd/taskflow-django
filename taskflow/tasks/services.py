from .firebase_config import db
import uuid
from datetime import datetime




def iniciar_sesion(email, password):

    users = db.collection("users").stream()

    for doc in users:

        user_data = doc.to_dict()

        if user_data["email"] == email and user_data["password"] == password:

            return {
                "message": "Inicio de sesión exitoso",
                "user" : user_data
            }
        
    return {"error": "Credenciales inválidas"}



def crete_task(data):

    task_id = str(uuid.uuid4())

    task = {
        "task_id": task_id,
        "title": data["title"],
        "description": data["description"],
        "assigned_to": data["assigned_to"],
        "status": "pendiente",
        "priority": data["priority"],
        "due_date": data["due_date"],
        "created_at": datetime.now(),
    }

    db.collection("tasks").document(task_id).set(task)

    return task

def get_tasks():

    tasks = []

    docs = db.collection("tasks").stream()

    for doc in docs: 
        tasks.append(doc.to_dict())

    return tasks

def update_task_status(task_id, status):

    task_ref = db.collection("tasks").document(task_id)

    task_ref.upsate({
        "status": status
    })

    return {"message": "Estado de la tarea actualizado correctamente"}

def delete_task(task_id):

    db.collection("tasks").document(task_id).delete()

    return {"message": "Tarea eliminada correctamente"}