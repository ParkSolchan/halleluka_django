from django.urls import path
from . import views

urlpatterns = [
    # url이 '/no_spoiler/'인 경우 GameList 클래스에서 처리하도록 호출
    path('', views.GameList.as_view())
]
