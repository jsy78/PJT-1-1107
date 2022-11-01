from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    articles = Article.objects.order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid:
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, "글 작성이 완료되었습니다.")
            return redirect("articles:index")
    else:
        form = ArticleForm()
        context = {
            "form": form,
        }
    return render(request, "articles/form.html", context)


def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "글이 수정되었습니다.")
                return redirect("articles:detail", article.pk)
        else:
            form = ArticleForm(instance=article)
            context = {
                "form": form,
            }
        return render(request, "articles/form.html", context)
    else:
        messages.warning(request, "글 작성자만 수정이 가능합니다.")
        return redirect("articles:detail", article.pk)


@login_required
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == "POST":
            article.delete()
            messages.success(request, "성공적으로 삭제되었습니다.")
            return redirect("articles:index")
        return render(request, "articles/detail.html")
    else:
        messages.warning(request, "권한이 없습니다. 작성자만 삭제 가능합니다.")
        return redirect("articles:detail", article.pk)


@login_required
def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = article.user
        comment.save()
        return redirect("articles:detail", article.pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
            return redirect("articles:detail", article_pk)
    else:
        messages.warning(request, "댓글 작성자만 삭제 가능합니다.")
        return redirect("articles:detail", article_pk)


@login_required
def likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect("articles:detail", article_pk)
