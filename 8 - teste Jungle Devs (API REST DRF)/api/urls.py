from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('articles/', views.articlesList, name='articlesList'),
    path('articles/<int:id>/', views.articlesDetail, name='articlesDetail'),

    path('login/', obtain_auth_token, name='login'),
    path('sign-up/', views.register, name='register'),
]