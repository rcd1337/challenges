from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

#app_name = "auction"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.cats, name="categories"),
    path("category/<str:category>", views.cat, name="category"),
    path("submit_comment", views.submit_comment, name="submit_comment"),
    path("close_listing", views.close_listing, name="close_listing")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)