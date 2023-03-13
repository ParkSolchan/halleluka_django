from django.contrib import admin
from .models import Post, Category, Tag

admin.site.register(Post)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin) :
    # Category 모델의 name 필드에 값이 입력됐을때, 자동으로 slug가 만들어지는 코드
    prepopulated_fields = {'slug': ('name', )}
class TagAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
