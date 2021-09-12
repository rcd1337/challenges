from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ArticleSerializer, ArticleSerializerAnonymous, RegistrationSerializer
from .models import Article, User, Token


@api_view(['GET',])
def articlesList(request):

    slug = request.GET.get('category', '')
    if slug:
        queryset = Article.objects.filter(slug=slug)
    else:
        queryset = Article.objects.all()

    serializer = ArticleSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(['GET', ])
def articlesDetail(request, id):

    try:
        queryset = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return Response(status=404)

    if request.user.is_authenticated:
        serializer = ArticleSerializer(queryset, many=False)
        return Response(serializer.data)

    serializer = ArticleSerializerAnonymous(queryset, many=False)
    
    return Response(serializer.data)


@api_view(['POST', ])
def register(request):

    serializer = RegistrationSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        new_user = serializer.save()
        data['response'] = f"successfully registered new user"
        data['username'] = new_user.username
        token = Token.objects.get(user=new_user).key
        data['token'] = token
        return Response(data, status=201)

    return Response(serializer.errors, status=400)
