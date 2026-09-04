from django import forms
from .models import Article, User, Comment
from django.contrib.auth.forms import UserCreationForm

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "is_published"]
        widgets = {
            "content": forms.Textarea(attrs={"rows":10})
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email"
    )

    class Meta:
        model=User
        fields=(
            "username",
            "email",
            "password1",
            "password2"
        )
    
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["content"]
        widgets={
            "content" : forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Напишите ваш комментарий"
                }
            )
        }
        labels = {
            "content": ""
        }