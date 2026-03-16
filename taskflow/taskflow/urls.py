from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("api/", include("tasks.urls")),
    path('admin/', admin.site.urls),

]
