from django.shortcuts import render
from boardapp.models import Board
from django.http import HttpResponse
from django.core.paginator import Paginator
from disposalapp.api import get_WasteMedicine_dict
# Create your views here.

def index(request):
    rsBoard = Board.objects.all().order_by('-b_no')
    page = int(request.GET.get('page', 1))
    pagenator = Paginator(rsBoard, 5)
    page_obj = pagenator.get_page(page)
    context = {'rsBoard' : page_obj}
    
    res = get_WasteMedicine_dict()
    
    return render(request,
                    "mainapp/index.html",
                    {"rsBoard" : page_obj, 'res' : res})
