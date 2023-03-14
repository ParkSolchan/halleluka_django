from django.shortcuts import render, redirect
# models.py 에 선언된 Post 객체를 임포트
from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
# dispatch() 메소드를 사용하기 위함
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

from django.shortcuts import get_object_or_404

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

    # 페이지 네이션 - 한번에 몇개를 보여줄지
    paginate_by = 5

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
        context['comment_form'] = CommentForm

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

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView) :
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form) :
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

                # POST 방식으로 전달된 정보 중에서 name이 tags_str 인 input값을 가져옴
            tags_str = self.request.POST.get('tags_str')
            if tags_str :
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list :
                    t = t.strip()
                    # 이 값을 name으로 갖는 태그가 있다면 가져오고, 없다면 새로만든다 (upsert)
                    # 첫번째 인자 (Tag) : Tag 모델의 인스턴스
                    # 두번째 인자 (is_tag_create) : 새로 생성되었는지 나타내는 bool값
                    tag, is_tag_created = Tag.objects.get_or_create(name = t)
                    if(is_tag_created) :
                        # 새로 만들어진 태그라면 slug값을 생성해주어야함
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    # self.object : 지금 생성된 포스트
                    self.object.tags.add(tag)

            return response
        else :
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView) :
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    # CreateView, UpdateView 는 모델명_form.html 를 찾아서 사용하기 때문에 수종으로 바꿔주어야한다.
    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs) :
        context = super(PostUpdate, self).get_context_data()
        # Post 레코드 (self.object로 가져온)에 tags가 존재하면 이 tags의 name을 리스트 형태로 담는다.
        if self.object.tags.exists() :
            tags_str_list = list()
            for t in self.object.tags.all() :
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def dispatch(self, request, *args, **kwargs) :
        # 방문자(request.user) 는 로그인한 상태여야 함
        # self.get_object() 는 Post.objects.get(pk=pk) 와 같은 역할
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            # 권한없음 에러 ( 403 에러 출력 )
            raise PermissionDenied
    
    def form_valid(self, form) :
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str :
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list :
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created :
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

class CommentUpdate(LoginRequiredMixin, UpdateView) :
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

def category_page(request, slug) :
    if slug == 'no_category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    # category = Category.objects.get(slug=slug)
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )

def tag_page(request, slug) :
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )

def new_comment(request, pk) :
    if request.user.is_authenticated :
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST' :
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() :
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else :
                return redirect(post.get_absolute_url())
        else :
            raise PermissionDenied

def delete_comment(request, pk) :
    # deleteView 를 사용하면 진짜 삭제할것인지 확인하는 페이지로 이동하기 때문에 페이지 이동을 하지 않기 위해서 모달형태로 구현
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author :
        comment.delete()
        return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied