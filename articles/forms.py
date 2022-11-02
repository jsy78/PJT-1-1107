from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "image", "grade", "location", "foodType"]
        labels = {
            "title": "가게 이름",
            "content": "후기",
            "grade": "평점",
            "location": "위치",
            "image": "사진 첨부",
            "foodType": "종류",
        }
        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "maxlength": "1",
                    "max": "5",
                    "min": "1",
                }
            ),
        }
        exclude = ("user",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
