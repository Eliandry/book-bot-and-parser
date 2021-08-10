from django.shortcuts import render
from django.views.generic import View
import requests
from bs4 import BeautifulSoup
from .models import *
from django.http import HttpResponseRedirect


def main(request):
    if request.method=='POST':
        url=request.POST.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('table', class_='island')

        for i in quotes:
            name = i.find('div', class_='book_name').text

            author = i.find('span', class_='desc2').text

            k = i.find_all('div', class_='desc_box')[1]
            genre = k.find_all('span', class_='desc2')[0].text
            genre = [s.strip() + ',' for s in genre.split(',') if s.strip()]
            description = i.find_all('div', 'description')[1].text

            a = i.find('div', class_='lt25')
            try:
                s = a.find_all('a')[0]
            except:
                continue
            url = 'https://www.litmir.me' + s.get('href')
            if '/bd/' in url:
                url = 'недоступно'
            imgs = i.find('img', 'lt32 lazy')
            img = 'https://www.litmir.me' + imgs.get('data-src')

            book=Book.objects.create(name=name,author=author,url=url,description=description)
            for i in genre:
                f=i.replace('.','')
                o,_=Genre.objects.get_or_create(name=f)
                book.genre.add(o)
            book.save()
    return render(request,'main.html')