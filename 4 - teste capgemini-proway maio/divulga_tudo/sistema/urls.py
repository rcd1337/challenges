from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastrar_anuncio", views.ad, name="ad"),
    path("cadastrar_cliente", views.client, name="client"),
    path("relatorio", views.report, name="report"),
    path("relatorios", views.reports, name="reports"),
]