from api.viewsets import ArticleViewset, AuthorViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('articles', ArticleViewset)
router.register('authors', AuthorViewset)