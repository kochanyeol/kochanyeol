"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

pl_list = [
    {"title": "아스날", "main": "사카"},
    {"title": "맨시티", "main": "홀란드"},
    {"title": "맨유", "main": "브페"},
    {"title": "AV", "main": "존 맥긴"},
]

def index(request):
    return HttpResponse('<h1>hello</h1>')

def book_list(request):
    # book_text = ''
    #
    # for i in range(0, 10):
    #     book_text += f'book {i}<br>'

    return render(request, 'book_list.html', {'range': range(0, 10)})

def book(request, num):
    return render(request, 'book_detail.html', {'num': num})

def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다.')

def python(request):
    return HttpResponse('python 페이지 입니다.')

def premier_league(request):
    # pl_titles = [f'<a href="/pl/{index}/">{pl["title"]}</a>' for index, pl in enumerate(pl_list)]

    # pl_titles = []
    # for pl in pl_list:
    #     pl_titles.append(pl['title'])

    # response_text =  '<br>'.join(pl_titles)
    # return HttpResponse(response_text)
    return render(request, 'pls.html', {'pl_list': pl_list})

def pl_detail(request, index):
    if index > len(pl_list) - 1:
        raise Http404

    pl = pl_list[index]

    return render(request, 'pl.html', {'pl': pl})

def multiplication(request):
    return HttpResponse('구구단 페이지 입니다.')

def multiplication_list(request, num):
    if num < 2:
        return redirect('/multiplication/2/')
    context = {"num": num, "gugu": [num * i for i in range(1, 10)]}

    return render(request, 'multiplication_list.html', context)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/python/', python),
    path('language/<str:lang>/', language),
    path('pl/', premier_league),
    path('pl/<int:index>/', pl_detail),
    path('multiplication/', multiplication),
    path('multiplication/<int:num>/', multiplication_list),
]
