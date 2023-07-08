from django.shortcuts import render
from .api import get_WasteMedicine_dict, get_city_list
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.

def get_dictList2(request):
    res = get_WasteMedicine_dict()
    context = {'res': res}
    return render(request, 
                "disposalapp/disposal_list.html",
                context)
    
def get_dictList(request):
    try:
        now_page = request.GET.get("page", "1")
        now_page = int(now_page)
        city = request.GET.get("city", "")
    except:
        now_page = 1
        city = ""

    if city == 'no':
        city = ""

    city_list = list(city.split(','))
    res = get_WasteMedicine_dict()

    if city == '' and '광주전체' not in city_list:
        city_list.append('광주전체')

    for li in city_list:
        if li == '광주전체':
            res = get_WasteMedicine_dict()
        elif li != '':
            res = get_city_list(city_list, res)
    
    
    total_count = len(res)
    row = 10
    now_page = int(now_page)
    start_page = int((now_page-1) / row) * row+1
    end_page = start_page + 9
    
    ## 마지막페이지 처리 추가
    if start_page + 9 > int((total_count-1)/row)+1 :
        end_page = int((total_count-1)/row) + 1

    is_prev = False
    is_next = False
    
    
    # if start_page > 0 :
    if start_page > 1 :
        is_prev = True
    if end_page < int((total_count-1) / row) + 1 :
        is_next = True
        
    ## 코드 추가
    # 한페이지마다 보여줄 범위값 추출
    if total_count > now_page*row + 1:
        res_end = now_page*row + 1
        res_start = res_end-row
    else : 
        res_end = total_count + 1
        res_start = (now_page-1)*row
    
    res_datas = []
    for i in range(res_start,res_end):
        res_datas.append(res[i])

    context = {
                "is_prev" : is_prev,
                "is_next" : is_next,
                "start_page" : start_page,
                # "page_range" : range(start_page, end_page ),
                "page_range" : range(start_page, end_page+1 ),
                "res_datas": res_datas,
                "city_list" : city,
                "total_count" : total_count,
                "res_range": range(res_start, res_end),
                "now_page" : now_page}
        
    return render(
        request, "disposalapp/disposal_list.html", context
    )

    
def get_map(request):
    return render(request,
                "disposalapp/map_popup.html",
                {})
    
def get_dictList_main(request):
    res = get_WasteMedicine_dict()
    context = {'res': res}
    return render(request, 
                "disposalapp/include/disposal_list_main.html",
                context)

