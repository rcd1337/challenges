from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name="index"),
    path("cadastro", views.cadastro, name="cadastro"),
    path("pre_cadastro_sala", views.pre_cadastro_sala, name="pre_cadastro_sala"),
    path("cadastro_sala", views.cadastro_sala, name="cadastro_sala"),
    path("cadastro_cafe", views.cadastro_cafe, name="cadastro_cafe"),
    path("consulta", views.consulta, name="consulta"),
    path("consulta_sala", views.consulta_sala, name="consulta_sala"),
    path("consulta_cafe", views.consulta_cafe, name="consulta_cafe")
] 