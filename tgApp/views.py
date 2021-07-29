from django.views.generic import ListView, DetailView, View
from .models import *
import requests
from bs4 import BeautifulSoup
import re
from tgApp.models import *
from django.conf import settings

class MainView(View):
    def post(self,request):
        url=request.POST.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('table', class_='island')

        for i in quotes:
            name = i.find('div', class_='book_name').text

            author = i.find('span', class_='desc2')

            k = i.find_all('div', class_='desc_box')[1]
            genre = k.find_all('span', class_='desc2')[0].text

            description = i.find_all('div', 'description')[1].text

            a = i.find('div', class_='lt25')
            s = a.find_all('a')[0]
            url = 'https://www.litmir.me/' + s.get('href')
            if '/bd/' in url:
                url = 'недоступно'
            imgs = i.find('img', 'lt32 lazy')
            img = 'https://www.litmir.me/' + imgs.get('data-src')
