from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus       #quote_plus includes the required symbols in the url(e.g. +,%)
from .import models
# Create your views here.

BASE_CRAIGLIST_URL='https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request,'index.html')

def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_CRAIGLIST_URL.format(quote_plus(search))
    page=requests.get(final_url)
    soup=BeautifulSoup(page.content,'html.parser')
    post_listings=soup.find_all('li',{'class':'result-row'})
    final_postings=[]
    for post in post_listings:
        post_title=post.find(class_='result-title').text
        print(post_title)
        post_url=post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price='N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url=BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url='https://craiglist.org/images/peace.jpg'

        final_postings.append((post_title,post_url,post_price,post_image_url))

    searchList={
        'search':search,
        'final_postings':final_postings,
    }
    return render(request, 'new_search.html',searchList)