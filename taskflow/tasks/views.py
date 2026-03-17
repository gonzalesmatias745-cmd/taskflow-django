from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import firebase_admin
from firebase_admin import credentials, firestore


# inicializar firestore
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()



# REGISTRO DE USUARIO


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def registrar_usuario(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Datos incompletos"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "El usuario ya existe"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # guardar en firestore
    db.collection("usuarios").add({
        "username": username,
        "email": email
    })

    return Response({
        "message": "Usuario registrado correctamente"
    })



# LOGIN


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def iniciar_sesion(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Credenciales inválidas"},
            status=401
        )

    login(request, user)

    return Response({
        "message": "Inicio de sesión exitoso"
    })



# CREAR TAREA


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def crear_tarea(request):

    titulo = request.data.get('title')
    descripcion = request.data.get('description')

    if not titulo:
        return Response(
            {"error": "El titulo es obligatorio"},
            status=400
        )

    db.collection("tareas").add({
        "titulo": titulo,
        "descripcion": descripcion
    })

    return Response({
        "message": "Tarea creada correctamente"
    })



# LISTAR TAREAS


@api_view(['GET'])
def listar_tareas(request):

    tareas_ref = db.collection("tareas")
    docs = tareas_ref.stream()

    tareas = []

    for doc in docs:
        tarea = doc.to_dict()
        tarea["id"] = doc.id
        tareas.append(tarea)

    return Response(tareas)



# ACTUALIZAR TAREA


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([AllowAny])
def actualizar_tarea(request, task_id):

    titulo = request.data.get("titulo")
    descripcion = request.data.get("descripcion")

    tarea_ref = db.collection("tareas").document(task_id)

    tarea_ref.update({
        "titulo": titulo,
        "descripcion": descripcion
    })

    return Response({
        "message": "Tarea actualizada correctamente"
    })

# ELIMINAR TAREA

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def eliminar_tarea(request, task_id):

    db.collection("tareas").document(task_id).delete()

    return Response({
        "message": "Tarea eliminada correctamente"
    })