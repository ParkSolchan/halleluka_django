from django.shortcuts import render
from django.views.generic import ListView
from .models import Game, Category
from bs4 import BeautifulSoup as bs
from selenium import webdriver

# Create your views here.
class GameList(ListView) :
    model = Game
    ordering = '-pk'

    paginate_by = 20

    def get_context_data(self, **kwargs) :
        context = super(GameList, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context
    
    def get_game_data(self) :
        driver = webdriver.Chrome('c:/Users/parksolchan/Downloads/chromedriver_mac_arm64/chromedriver')
        url_lck = 'https://game.naver.com/esports/League_of_Legends/videos/league/lck'
        driver.get(url_lck)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        