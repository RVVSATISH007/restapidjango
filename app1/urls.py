from django.urls import path
from .views import FetchAndStoreNewsAPI ,ArticleListAPI

urlpatterns = [
    path("api/fetch-news/", FetchAndStoreNewsAPI.as_view()),
     path("articles/", ArticleListAPI.as_view()),
]
