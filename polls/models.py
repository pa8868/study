from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
# 게시글(Post)엔 제목(postname), 내용(contents)이 존재합니다
class Post(models.Model):
    postname = models.CharField(max_length=50)
    mainphoto = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    contents = models.TextField()
    #created_at = models.DateTimeField(auto_now_add=True,null=True)

    # 게시글의 제목(postname)이 Post object 대신하기
    def __str__(self):
        return self.postname

class Get(models.Model):
    postname = models.CharField(max_length=200)  # 제목 필드
    contents = models.TextField()  # 내용 필드
    mainphoto = models.ImageField(upload_to='images/', blank=True, null=True) 

    def __str__(self):
        return self.postname
    
class Post_Comment(models.Model):
    b_num = models.IntegerField(default=0,null=False)
    comment = models.TextField(max_length=255,null=False)
    name = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=254,null=False)
    created_at = models.DateTimeField(null=True, blank=True)
    del_comment = models.BooleanField(default=False,null=False)
    class Meta:
        db_table = 'polls_comments'