from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

class Category(models.Model) :
    name = models.CharField(max_length=50, unique=True)
    # 사람이 읽을수 있는 텍스트로 고유 url을 만들고 싶을때 사용하는 SlugFiled
    # unique=True로 설정해 다른 카테고리가 동일한 slug를 가질수 없게 하고
    # SlugField는 한글을 지원하지 않지만, allow_unicode=True를 통해서 한글로도 만들수 있게 함
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return f'/blog/category/{self.slug}/'
    # Category의 복수형을 Categorys라고 쓰는것을 수정해주는 코드
    # 복수형을 직접 지정
    class Meta:
        verbose_name_plural = 'Categories'
class Tag(models.Model) :
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return f'/blog/tag/{self.slug}/'

class Post(models.Model) :
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    # content = models.TextField()
    content = MarkdownxField()

    # blank=True :  해당 항목은 필수값이 아니다는 선언
    head_image = models.ImageField(upload_to='blog/image/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user 테이블에 유저 정보 삭제시 작성글도 같이 날림
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # user 테이블에 유저 정보가 삭제되면 작성글에 author가 null 로 변함
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # ManyToManyField 는 null=True 가 기본값
    tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self) :
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self) :
        return f'/blog/{self.pk}/'

    def get_file_name(self) :
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self) :
        return self.get_file_name.split('.')[-1]

    def get_content_markdown(self) :
        return markdown(self.content)
        
    def get_avatar_url(self) :
        if self.author.socialaccount_set.exists() :
           return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return f'https://doitdjango.com/avatar/id/1469/be9027120fdb9b94/svg/{self.author.email}'
        
class Comment(models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 처음 생성될때의 시간을 저장
    modified_at = models.DateTimeField(auto_now=True) # 저장 될때의 시간을 저장

    def __str__ (self) :    # 작성자 명과 content 내용을 출력하는 __str__ 함수
        return f'{self.author}::{self.content}'

    def get_absolute_url(self) :
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self) :
        if self.author.socialaccount_set.exists() :
           return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return f'https://doitdjango.com/avatar/id/1469/be9027120fdb9b94/svg/{self.author.email}'
        
