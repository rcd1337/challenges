from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import ArticleSerializer, AuthorSerializer
from .models import Article, User


class ArticleViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class AuthorViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = AuthorSerializer