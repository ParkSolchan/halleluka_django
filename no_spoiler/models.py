from django.db import models

# Create your models here.
class Category(models.Model) :
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name
    
    def get_absolute_url(self) :
        return f'/no_spoiler/category/{self.slug}/'

class Game(models.Model) :
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.CharField(max_length=500)

    played_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) :
        return f'[{self.pk}]{self.category} :: {self.title}'

