from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    articles = Article.objects.order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "articles/index.html", context)


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    context = {
        "article": article,
        "comments": article.comment_set.all(),
        "comment_form": comment_form,
    }
    if request.user == article.user:
        context["user"] = True
    else:
        context["user"] = False
    # 리턴된 HttpResponse 객체를 response 변수에 할당
    response = render(request, "article/detail.html", context)
    # 조회수 기능(쿠키이용)
    # 쿠키 만료시간 설정
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    # 쿠키 만료시간 설정 끝
    # 남은 시간 초단위 저장
    max_age = expire_date.total_seconds()
    # request 에서 hitboard라는 쿠키값 가져오기, 없으면 _ 로 가져오기
    cookie_value = request.COOKIES.get("hitboard", "_")
    # 쿠키값에 해당 게시글의 번호가 없을 경우, 쿠키에 게시글의 번호를 추가하고 조회수를 +1
    if f"_{pk}_" not in cookie_value:
        cookie_value += f"{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        article.hits += 1
        article.save()
    # response객체return
    return response


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


def paginator(request):
    article_list = Article.objects.all().order_by("-pk")  # 데이터 역순 정렬
    page = request.GET.get("page", "1")  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(article_list, "2")  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    paginated_article_lists = paginator.get_page(page)  # 페이지 번호를 받아 해당 페이지를 리턴
    context = {
        "article_list": article_list,
        "paginated_article_lists": paginated_article_lists,
    }

    return render(request, "articles/index.html", context)
