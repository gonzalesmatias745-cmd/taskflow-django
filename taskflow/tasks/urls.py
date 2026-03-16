from django.urls import path
from .views import *

urlpatterns = [

    path('register/', registrar_usuario),
    path('login/', iniciar_sesion),

    path('tasks/create/', crear_tarea),
    path('tasks/', listar_tareas),

    path('tasks/<str:task_id>/update/', actualizar_tarea),
    path('tasks/<str:task_id>/delete/', eliminar_tarea),

]