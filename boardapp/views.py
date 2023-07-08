from django.shortcuts import render, redirect
from django.http import HttpResponse
from boardapp.models import Board
from boardapp.forms import RegistForm
from django.core.paginator import Paginator

# Create your views here.

# def home(request):
#     return render(request, 'boardapp/home.html', {})

# def board(request):
#     rsBoard = Board.objects.all()
#     return render(request, 'boardapp/board_list.html', {'rsBoard':rsBoard})


# 다른거 따라하던 index
# def index(request):
#     board_list = Board.objects.all().order_by('-b_no')
#     context = {'board_list' : board_list}
#     return render(request, 'boardapp/index.html', context)


def regist(request):
    
    user = request.session.get('user')
    # if not request.session.get('user'):
    #     return redirect('/accounts/login')

    if request.method =='POST': 
        form = RegistForm(request.POST)
        if form.is_valid():
            # user_id = request.session.get('user')
            # user = User.objects.get(pk=user_id)

            board=Board()
            board.b_title = form.cleaned_data['b_title']
            board.b_note = form.cleaned_data['b_note']
            board.b_writer = user
            board.b_writer = form.cleaned_data[user]
            board.save()

            return redirect('boardapp/board_list.html')
    # else:
    #     form = RegistForm()
    return render(request, 'boardapp/regist_form.html', { 'form' : form })
    
    
    
    board_list = Board.objects.all().order_by('-b_no')
    context = {'board_list' : board_list}
    return render(request, 'boardapp/regist_form.html', context)


def board_list(request):
    rsBoard = Board.objects.all().order_by('-b_no')
    page = int(request.GET.get('page', 1))
    pagenator = Paginator(rsBoard, 5)
    page_obj = pagenator.get_page(page)
    context = {'rsBoard' : page_obj}
    
    
    return render(request, 'boardapp/include/board_list.html', context)
    
    
    return HttpResponse(page_obj)
    # return render(request, 
    #                 'boardapp/include/board_list.html', 
    #                 {'rsBoard':rsBoard, 
    #                  'boards':boards })


def detail(request, b_no):
    # 상세보기
    board_list = Board.objects.get(b_no=b_no)
    context = {'board_list': board_list}
    return render(request, 'boardapp/detail.html', context)
