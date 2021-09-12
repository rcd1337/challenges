from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("w/new", views.new, name="new"),
    path("w/edit", views.edit, name="edit"),
    path("w/random", views.randompage, name="randompage"),
    path("<str:wikipage>", views.page, name="wikipage")
]
