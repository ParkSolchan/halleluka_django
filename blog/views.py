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

def single_post_page(request, pk) :
    # .get(pk=pk) : 괄호안의 조건을 만족하는 Post레코드를 가져오는 함수
    #  ==> Post 모델의 pk 필드값이 매개변수 pk와 같은 레코드만을 호출하라는 의미
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )