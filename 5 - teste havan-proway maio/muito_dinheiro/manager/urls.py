from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastrar_cliente", views.add_client, name="add_client"),
    path("cadastrar_operacao", views.add_operation, name="add_operation"),
    path("relatorios", views.reports, name="reports")
]