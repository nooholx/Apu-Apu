"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views

app_name = 'www_board'

urlpatterns = [
    
    # ### http://127.0.0.1:8000/board/board_list
    path('board_list/', views.board_list, name = 'board_list'),
    
    # ### http://127.0.0.1:8000/board/1, 2, 3 ... (게시글번호에 따라)
    path('<int:b_no>/', views.detail, name ='detail'),
    
    
]
