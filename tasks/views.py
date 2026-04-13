from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .firebase_config import db





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

    titulo = request.data.get('titulo')
    descripcion = request.data.get('descripcion')
    estado = request.data.get('estado', 'pendiente')

    if not titulo:
        return Response(
            {"error": "El titulo es obligatorio"},
            status=400
        )

    db.collection("tareas").add({
        "titulo": titulo,
        "descripcion": descripcion,
        "estado": estado
    })

    return Response({
        "message": "Tarea creada correctamente"
    })



# LISTAR TAREAS


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
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
    estado = request.data.get("estado") 

    tarea_ref = db.collection("tareas").document(task_id)

    # Actualizamos solo lo que venga en el JSON
    datos = {}
    if titulo: datos["titulo"] = titulo
    if descripcion: datos["descripcion"] = descripcion
    if estado: datos["estado"] = estado 

    tarea_ref.update(datos)

    return Response({"message": "Tarea actualizada correctamente"})



# ELIMINAR TAREA

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def eliminar_tarea(request, task_id):

    db.collection("tareas").document(task_id).delete()

    return Response({
        "message": "Tarea eliminada correctamente"
    })



# OBTENER CANTIDAD DE TAREAS (ESTADISTICA) 
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def cantidad_tareas(request):
    try:
        tareas_ref = db.collection("tareas")
        # Traemos los documentos una sola vez
        docs = tareas_ref.stream()

        # Inicializamos contadores
        completada = 0
        en_progreso = 0
        pendientes = 0
        cantidad_total = 0

        # En un solo recorrido calculamos todo
        for doc in docs:
            cantidad_total += 1
            tarea = doc.to_dict()
            
            # Es importante que el string coincida exactamente con lo que guardas
            estado = tarea.get("estado", "pendiente").lower()  # Convertimos a minúsculas para evitar problemas de mayúsculas
            
            if estado == "completada":
                completada += 1
            elif estado == "en progreso":
                en_progreso += 1
            else:
                pendientes += 1 

        return Response({
            "cantidad": cantidad_total,
            "completada": completada,
            "en_progreso": en_progreso,
            "pendientes": pendientes
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener estadísticas: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
