from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postname', 'contents', 'mainphoto']  # 수정할 필드를 지정
