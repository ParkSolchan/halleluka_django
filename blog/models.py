from django.db import models
from django.contrib.auth.models import User
import os

class Category(models.Model) :
    name = models.CharField(max_length=50, unique=True)
    # 사람이 읽을수 있는 텍스트로 고유 url을 만들고 싶을때 사용하는 SlugFiled
    # unique=True로 설정해 다른 카테고리가 동일한 slug를 가질수 없게 하고
    # SlugField는 한글을 지원하지 않지만, allow_unicode=True를 통해서 한글로도 만들수 있게 함
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name

    # Category의 복수형을 Categorys라고 쓰는것을 수정해주는 코드
    # 복수형을 직접 지정
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model) :
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

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
    def __str__(self) :
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self) :
        return f'/blog/{self.pk}/'

    def get_file_name(self) :
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self) :
        return self.get_file_name.split('.')[-1]