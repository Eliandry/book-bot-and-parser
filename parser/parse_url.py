import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.litmir.me/bs/?g=sg136'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
href=[]
quotes = soup.find_all('table', class_='island')

for i in quotes:
    name=i.find('div',class_='book_name').text

    author=i.find('span',class_='desc2')

    k=i.find_all('div',class_='desc_box')[1]
    genre=k.find_all('span',class_='desc2')[0].text

    description=i.find_all('div','description')[1].text

    a=i.find('div',class_='lt25')
    s=a.find_all('a')[0]
    url=s.get('href')
    if '/bd/' in url:
        url='недоступно'
