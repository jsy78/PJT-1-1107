from django.shortcuts import render
from articles.models import Article


def main(request):
    articles = Article.objects.order_by("-like_users")
    context = {
        "articles": articles,
    }
    return render(request, "main.html", context)

def new(request):
    articles = Article.objects.order_by("-created_at")
    context = {
        "articles": articles,
    }
    return render(request, "main.html", context)

def good(request):
    articles = Article.objects.order_by("-like_users")
    context = {
        "articles": articles,
    }
    return render(request, "main.html", context)

def hit(request):
    articles = Article.objects.order_by("-hits")
    context = {
        "articles": articles,
    }
    return render(request, "main.html", context)