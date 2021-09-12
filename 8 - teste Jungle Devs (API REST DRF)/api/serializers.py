from rest_framework import serializers
from .models import Article, User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'picture']

class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source='user', many=False, read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'author', 'category', 'title', 'summary', 'firstParagraph', 'body']


class ArticleSerializerAnonymous(serializers.ModelSerializer):
    author = AuthorSerializer(source='user', many=False, read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'author', 'category', 'title', 'summary', 'firstParagraph']

class ArticleSerializerList(serializers.ModelSerializer):
    author = AuthorSerializer(source='user', many=False, read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'author', 'category', 'title', 'summary']
        

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'picture']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user