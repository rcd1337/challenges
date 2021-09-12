from django.urls import path
from . import views

urlpatterns = [
    path("<str:number>", views.extenso, name="extenso"),
    path("", views.index, name="index")
]