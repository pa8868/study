from django.urls import path
from . import views
from polls.views import blog, posting

from django.conf.urls.static import static
from django.conf import settings

#해당 app에서 url을 만들경우, .으로 표시
# 사용할 메서드 목록을 url과 연결(라우팅)

app_name = 'polls'

urlpatterns = [
    path("", views.index, name="index"),
    path('blog/',views.blog,name='blog'),
    path('blog/<int:pk>',views.posting, name="posting"),
    path('blog/new_post/',views.new_post, name="new_post"),
    path('blog/remove/<int:pk>/',views.remove_post, name='remove_post'),
    path('blog/post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/edit_post/<int:pk>/', views.posting, name='posting'),
    path('blog/posting_detail/<int:pk>/',views.posting_detail,name='posting_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)