from django.test import TestCase, Client
from .models import Game, Category
from bs4 import BeautifulSoup as bs
from django.contrib.auth.models import User
from selenium import webdriver

# Create your tests here.
class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_luka = User.objects.create_user(username='luka', password='1234')
        self.user_luka.is_staff = True
        self.user_luka.save()

        self.category_lol = Category.objects.create(name='lol', slug='lol')

        self.browser = webdriver.Chrome('c:/Users/parksolchan/Downloads/chromedriver_mac_arm64/chromedriver')
    
    def test_selenium(self) :
        self.browser.get('http://www.naver.com')
        self.assertIn('NAVER', self.browser.title)
