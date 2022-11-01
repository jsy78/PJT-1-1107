from django.shortcuts import render
from articles.models import Article

def main(request):
    articles = Article.objects.order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "main.html", context)