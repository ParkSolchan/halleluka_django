from django.shortcuts import render
# models.py 에 선언된 Post 객체를 임포트
from .models import Post

# Create your views here.
def index(request) :
    # order_by를 사용하면 pk값의 역순으로 정렬됨
    posts = Post.objects.all().order_by('-pk');

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts
        }
    )