# # views.py
# import requests
# from datetime import datetime
# from django.http import JsonResponse
# from django.db import IntegrityError

# from .models import Article

# API_URL = "https://newsapi.org/v2/everything"
# API_KEY = "YOUR_API_KEY"


# def fetch_and_store_news(request):
#     params = {
#         "q": "tesla",
#         "sortBy": "publishedAt",
#         "apiKey": API_KEY
#     }

#     response = requests.get(API_URL, params=params)

#     if response.status_code != 200:
#         return JsonResponse({"error": "API fetch failed"}, status=400)

#     data = response.json()
#     articles = data.get("articles", [])

#     stored_articles = []

#     for item in articles:
#         try:
#             article = Article.objects.create(
#                 title=item.get("title"),
#                 description=item.get("description"),
#                 url=item.get("url"),
#                 source=item.get("source", {}).get("name"),
#                 published_at=datetime.fromisoformat(
#                     item.get("publishedAt").replace("Z", "+00:00")
#                 )
#             )

#             stored_articles.append({
#                 "title": article.title,
#                 "description": article.description,
#                 "url": article.url,
#                 "source": article.source,
#                 "published_at": article.published_at
#             })

#         except IntegrityError:
#             # Duplicate URL – ignore
#             pass

#     return JsonResponse({
#         "message": "Data stored successfully",
#         "count": len(stored_articles),
#         "data": stored_articles
#     })

# views.py
import requests
from datetime import datetime
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Article
from .serializers import ArticleSerializer

API_URL = "https://newsapi.org/v2/everything"
API_KEY = "bf0f8a03180045b18c06c405d4905b4d"


class FetchAndStoreNewsAPI(APIView):

    def get(self, request):
        params = {
            "q": "tesla",
            "sortBy": "publishedAt",
            "apiKey": API_KEY
        }

        response = requests.get(API_URL, params=params)

        if response.status_code != 200:
            return Response(
                {"error": "Failed to fetch external API"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = response.json()
        print(data)
        articles = data.get("articles", [])
        stored = []
        for item in articles:
            try:  
                article = Article.objects.create(
                    title=item.get("title"),
                    description=item.get("description"),
                    url=item.get("url"),
                    source=item.get("source", {}).get("name"),
                    published_at=datetime.fromisoformat(
                        item.get("publishedAt").replace("Z", "+00:00")
                    )
                )
                stored.append(article)

            except IntegrityError:
                # duplicate URL
                pass

        serializer = ArticleSerializer(stored, many=True)

        return Response({
            "message": "Data stored successfully",
            "count": len(serializer.data),
            "data": serializer.data
        }, status=status.HTTP_200_OK) 



class ArticleListAPI(APIView):
    """
    GET API – Fetch data ONLY from database
    """

    def get(self, request):
        articles = Article.objects.all().order_by("-published_at")

        serializer = ArticleSerializer(articles, many=True)

        return Response({
            "count": len(serializer.data),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


