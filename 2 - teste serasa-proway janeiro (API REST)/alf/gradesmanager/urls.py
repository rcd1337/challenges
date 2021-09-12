from django.urls import path

from . import views

urlpatterns = [
    # API Routes
    path("gabarito", views.gabarito, name="gabarito"),
    path("aluno", views.aluno, name="aluno"),
    path("resposta", views.resposta, name="resposta"),
    path("aprovados", views.aprovados, name="aprovados")
]