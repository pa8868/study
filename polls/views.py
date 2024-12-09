# polls/views.py

from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Post_Comment
from .forms import PostForm
from django.db.models import Q
from django.db import connection
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.method == "POST":
        if request.POST.get('action') == '세션삭제1':
            if 'email' in request.session:
                del request.session['email']
                del request.session['name']
            return redirect('accounts:login')
        if request.POST.get('action') == '세션삭제2':
            if 'email' in request.session:
                del request.session['email']
                del request.session['name']
            return redirect('accounts:login2')
    return render(request,'polls/index.html')

def blog(request):
    postlist = Post.objects.all()
    if not postlist:
        print("게시글이 없습니다.")
    return render(request, 'polls/blog.html', {'postlist':postlist})

def posting(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    #디비에 접근해서 댓글 테이블에서 접근한 게시글에 맞는 댓글을 불러와서 객체에 저장한다음 render에 뿌려주기
    comments = Post_Comment.objects.filter(b_num=pk, del_comment=False).order_by('created_at')
   
    if request.method == 'POST':
        # 수정 폼 처리
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('polls:posting', pk=post.pk)  # 수정 후 해당 게시글 페이지로 리다이렉트
        else:
            form = PostForm(instance=post)  # 수정할 게시글 데이터로 폼 생성

        return render(request, 'polls/posting.html', {'form': form, 'post': post})

        # 댓글 작성 처리 
    elif 'submit_comment' in request.POST:
        comment_content = request.POST.get('comment_content')
        if comment_content:
            # 새 댓글을 작성합니다
            Post_Comment.objects.create(
                b_num=pk,  # 게시글 번호 (댓글이 달린 게시글의 pk)
                comment=comment_content,  # 댓글 내용
                name=request.user.username,  # 작성자 이름 (예: 로그인한 사용자 이름)
                email=request.user.email,  # 작성자 이메일 (예: 로그인한 사용자 이메일)
            )
        return redirect('polls:posting', pk=post.pk)

        # 댓글 삭제 처리 ## <-
    elif 'delete_comment' in request.POST:
        comment_id = request.POST.get('comment_id')
        if comment_id:
            comment = get_object_or_404(Post_Comment, pk=comment_id, b_num=pk)
                # 댓글 삭제 (논리적 삭제)
            comment.del_comment = True
            comment.save()
            comment.refresh_from_db() ##
        return redirect('polls:posting', pk=post.pk)  # 댓글 삭제 후 해당 게시글 페이지로 리다이렉트
    

        # 삭제 폼 처리
    elif 'delete_post' in request.POST:
            post.delete()
            return redirect('polls:blog')  # 삭제 후 목록 페이지로 리다이렉트

    return render(request, 'polls/posting.html', {'post': post, 'form': form, 'comments': comments})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    posts = Post.objects.all().order_by('-created_at')
    post_number = list(posts).index(post) + 1  # 인덱스 + 1을 해서 번호 계산
    return render(request, 'polls/posting.html', {'post': post, 'post_number': post_number})

def new_post(request):
    if request.method == 'POST':
        if request.POST['mainphoto']:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        else:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        return redirect('/blog/')
    return render(request, 'polls/new_post.html')

def remove_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        # 게시글 삭제
        post.delete()
        return redirect('polls:blog')  # 삭제 후 블로그 목록으로 리다이렉트
    
    # GET 요청이면 삭제 폼을 보여줌
    return render(request, 'polls/remove_post.html', {'Post': post})

def blog(request):
    query = request.GET.get('q', '')  # 검색어를 GET 파라미터로 받음
    posts = Post.objects.all()

    # 검색어가 있을 경우 제목에 검색어가 포함된 게시글을 필터링
    if query:
        posts = posts.filter(Q(postname__icontains=query))  # 제목에 검색어가 포함된 게시글 필터링

    return render(request, 'polls/blog.html', {'postlist': posts, 'query': query})

def posting_detail(request, pk):
    # 게시글을 불러옵니다.
    post = get_object_or_404(Post, pk=pk)
    # 댓글 목록을 불러옵니다.
    
    # 댓글이 POST 요청으로 작성되었을 때
    if request.method == "POST":
        # 댓글을 작성하는 폼을 처리합니다.
        current_time = datetime.now()
        sql = f"Insert into polls_comments(b_num,comment,name,email,created_at,del_comment) Values('{pk}','{request.POST.get("content")}','{request.session.get("name")}','{request.session.get("email")}','{current_time.strftime("%Y-%m-%d %H:%M")}',0)"
        with connection.cursor() as cursor:
            cursor.execute(sql)

        # 댓글 저장 후 게시글 상세 페이지로 리디렉션
        return redirect('polls:posting', pk=post.pk)