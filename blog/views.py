# from django.shortcuts import render
# models.py 에 선언된 Post 객체를 임포트
from .models import Post, Category
from django.views.generic import ListView, DetailView

# Create your views here.

# ListView를 사용하는데 model은 Post이다.
class PostList(ListView):
    # django에서 제공하는 ListView 클래스는 모델명 뒤에 '_list'가 붙은 html파일을 기본 템플릿으로 사용하도록 설정되어 있다.
    # 즉 Post모델을 사용하면 post_list.html을 불러오는데 이를 해결하는 방법은
    # 1. post_list.html을 만들어서 그대로 사용하는 방법
    # 2. PostList클래스에서 template_name을 지정해주는 방법
    model = Post
    # template_name = 'blog/index.html'
    # pk값을 오름차순으로 보여주라는 명령어
    ordering = '-pk'

    def get_context_data(self, **kwargs) :
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
# def index(request) :
#     # order_by를 사용하면 pk값의 역순으로 정렬됨
#     posts = Post.objects.all().order_by('-pk');

#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts
#         }
#     )

# django에서 제공하는 DetailView는 '_detai'로 끝나는 파일을 이용함
class PostDetail(DetailView) :
    model = Post

    def get_context_data(self, **kwargs) :
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context

# def single_post_page(request, pk) :
#     # .get(pk=pk) : 괄호안의 조건을 만족하는 Post레코드를 가져오는 함수
#     #  ==> Post 모델의 pk 필드값이 매개변수 pk와 같은 레코드만을 호출하라는 의미
#     post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/single_post_page.html',()
#         {
#             'post': post,
#         }
#     )