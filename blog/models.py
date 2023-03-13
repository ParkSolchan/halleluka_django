from django.db import models
from django.contrib.auth.models import User
import os

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

    def __str__(self) :
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self) :
        return f'/blog/{self.pk}/'

    def get_file_name(self) :
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self) :
        return self.get_file_name.split('.')[-1]