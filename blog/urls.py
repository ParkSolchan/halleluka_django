from django.urls import path
# 현재 폴더에 있는 views.py 파일을 참조
from . import views

urlpatterns = [
    # /blog/ 뒤에 정수(int) 형태의 값이 붙는 url이라면 입력받은 정수 형태의 값을 pk로 받아서 single_post_page()함수로 보내겠다는 의미
    # path('<int:pk>/', views.single_post_page),
    # 입력된 url이 blog/ 로 끝난다면 참조한 views.py 에 정의되어 있는 index() 함수를 사용하겠다는 의미
    # path('', views.index),

    # url이 /blog/인 경우 PostList 클래스에서 처리하도록 호출
    path('', views.PostList.as_view()),
    # url이 'blog/정수/' 형태일 경우 PostDetail클래스를 이용하도록
    path('<int:pk>/', views.PostDetail.as_view()),

    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),

    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
]