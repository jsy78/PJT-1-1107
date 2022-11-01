from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(120, 80)],
        format="JPEG",
    )
    category = (
        ("한식", "한식"),
        ("일식", "일식"),
        ("중식", "중식"),
        ("양식", "양식"),
        ("분식", "분식"),
        ("치킨", "치킨"),
        ("아시안", "아시안"),
        ("패스트푸드", "패스트푸드"),
        ("디저트/카페", "디저트/카페"),
        ("기타", "기타"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_users"
    )
    bookmark_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="bookmark_users"
    )


class Comment(models.Model):
    content = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_articles",
    )
