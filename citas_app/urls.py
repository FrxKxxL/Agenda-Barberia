from django.urls import path
from citas_app import views

urlpatterns = [
    path("", views.panel_citas, name="panel_citas"),
    path("nueva/", views.nueva_cita, name="nueva_cita"),
    path("cita/<int:cita_id>/estado/<str:nuevo_estado>/", views.cambiar_estado, name="cambiar_estado"),
    path("cita/<int:cita_id>/eliminar/", views.borrar_cita, name="borrar_cita"),
]