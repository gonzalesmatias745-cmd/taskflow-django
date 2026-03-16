from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response    
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from firebase_config import db

import uuid
from datetime import datetime

# REGISTRAR USUARIO

@api_view(['POST'])

def registrar_usuario(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            "error": "Datos incompletos"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response ({
            "error": "El nombre de usuario ya existe"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        email=email, 
        password=password)
    
    return Response({
        "message": "Usuario registrado exitosamente",
        "user_id": user.id
    }, status=status.HTTP_201_CREATED)

#INICIAR SESION

@api_view(['POST'])
def iniciar_sesion(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:

        return Response({
            "error": "Credenciales inválidas"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    login(request, user)

    return Response({
        "message": "Inicio de sesión exitoso",
        "username": user.username
    })

#CERRAR SESION

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def cerrar_sesion(request):

    logout(request)

    return Response({
        "message": "Cierre de sesión exitoso"
    })

#CREAR TAREA

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_tarea(request):

    title = request.data.get("title")
    description = request.data.get("description")
    priority = request.data.get("priority")
    due_date = request.data.get("due_date")

    if not title:
        return Response({
            "error": "El título es obligatorio"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task_id = str(uuid.uuid4())

    task = {
        "task_id": task_id,
        "title": title,
        "description": description,
        "assigned_to": request.user.username,
        "status": "pendiente",
        "priority": priority,
        "due_date": due_date,
        "created_at": str(datetime.now())
    }

    db.collection("tasks").document(task_id).set(task)

    return Response ({
        "message": "Tarea creada exitosamente",
        "task": task
    })

#LISTAR TAREAS

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def listar_tareas(request):

    tasks = []

    docs = db.collection("tasks").stream()

    for doc in docs: 
        tasks.append(doc.to_dict())

        return Response(tasks)
    

#ACTUALIZAR ESTADO DE TAREA
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def actualizar_estado_tarea(request, task_id):

    new_status = request.data.get("status")

    if not new_status:
        return Response({
            "error": "El nuevo estado de la tarea es obligatorio"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task_ref = db.colleection("tasks").document(task_id)

    task_ref.update({
        "status": new_status
    })

    return Response({
        "message": "Estado de la tarea actualizado correctamente"
    })

#ELIMINAR TAREA

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def eliminar_tarea(request, task_id):

    db.collection("tasks").document(task_id).delete()

    return Response({
        "message": "Tarea eliminada correctamente"
    })