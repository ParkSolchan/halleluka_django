from django.urls import path
# 현재 폴더에 있는 views.py 파일을 참조
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_post_page),
    # 입력된 url이 blog/ 로 끝난다면 참조한 views.py 에 정의되어 있는 index() 함수를 사용하겠다는 의미
    path('', views.index),
]