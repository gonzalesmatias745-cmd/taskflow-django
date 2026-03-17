🧠 TaskFlow Django API

API REST desarrollada con Django + Django REST Framework para la gestión de usuarios y tareas, utilizando Firebase Firestore como base de datos.

📌 Características

✅ Registro de usuarios

🔐 Inicio de sesión

📝 Crear tareas

📋 Listar tareas

✏️ Actualizar tareas

🗑️ Eliminar tareas

☁️ Integración con Firebase Firestore

🛠️ Tecnologías utilizadas

Python 🐍

Django

Django REST Framework

Firebase Admin SDK

Firestore

⚙️ Instalación
1. Clonar el repositorio
git clone https://github.com/tu-usuario/taskflow-django.git
cd taskflow-django
2. Crear entorno virtual
python -m venv venv

Activar entorno:

Windows:

venv\Scripts\activate

Linux / Mac:

source venv/bin/activate
3. Instalar dependencias
pip install -r requirements.txt
4. Configurar Firebase

Ir a Firebase Console

Crear proyecto

Descargar archivo serviceAccountKey.json

Colocarlo en la raíz del proyecto

5. Migraciones
python manage.py migrate
6. Ejecutar servidor
python manage.py runserver
🔗 Endpoints
👤 Registro de usuario

POST /registrar/

{
  "username": "samuel",
  "email": "samuel@gmail.com",
  "password": "123456"
}
🔐 Login

POST /login/

{
  "username": "samuel",
  "password": "123456"
}
📝 Crear tarea

POST /tareas/

{
  "title": "Estudiar Django",
  "description": "Repasar API REST"
}
📋 Listar tareas

GET /tareas/

✏️ Actualizar tarea

PUT /tareas/{task_id}/

{
  "titulo": "Nuevo título",
  "descripcion": "Nueva descripción"
}
🗑️ Eliminar tarea

DELETE /tareas/{task_id}/

📁 Estructura del proyecto
taskflow-django/
│
├── taskflow/
│   ├── settings.py
│   ├── urls.py
│
├── tasks/
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│
├── serviceAccountKey.json
├── manage.py
└── requirements.txt