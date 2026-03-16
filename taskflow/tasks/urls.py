from django.urls import path
from .views import registrar_usuario, iniciar_sesion, listar_tareas, crear_tarea, actualizar_estado_tarea, eliminar_tarea

urlpatterns = [
    path("register/", registrar_usuario, name="registrar_usuario"),
    path("login/", iniciar_sesion, name="iniciar_sesion"),
    path("tasks/", listar_tareas, name="listar_tareas"),
    path("tasks/create/", crear_tarea, name="crear_tarea"),
    path("tasks/<str:task_id>/update_status/", actualizar_estado_tarea, name="actualizar_estado_tarea"),
    path("tasks/<str:task_id>/delete/", eliminar_tarea, name="eliminar_tarea"),

]