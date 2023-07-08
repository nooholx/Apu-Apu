from django.shortcuts import render
from django.http import HttpResponse
import requests
import io
import os
from google.cloud import vision

# Create your views here.

# search 함수들
def url_push(keyword, search_option):
    url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?serviceKey=2BAtuMGfsWORDJCneibKu/ZLiKB0RjrF4YJkdcJUn0ZLkC55h/R/tGqCPTh2wObTPR8Y1G343uVIqxYbFcU3UQ==&pageNo=1&numOfRows=10&type=json&'
    url = url + search_option + '=' + keyword
    return(url)

def url_page(keyword, search_option,page):
    url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?serviceKey=2BAtuMGfsWORDJCneibKu/ZLiKB0RjrF4YJkdcJUn0ZLkC55h/R/tGqCPTh2wObTPR8Y1G343uVIqxYbFcU3UQ==&numOfRows=10&type=json&pageNo='
    url = url + page + '&' + search_option + '=' + keyword
    return(url)

def response(url):
    response = requests.get(url)
    result = response.json()
    result = result['body']
    return(result)

# google ORC
def google_vision_orc(img_file):
    # 각자의 환경에 맞혀서 경로 확인해주세요
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/www/long-plexus-390002-c69c4740468f.json"
    client = vision.ImageAnnotatorClient()
    file_name = os.path.abspath(img_file)
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    texts = texts[0].description.split()
    return texts

###########################################################################################################
###  약 등록  ###
def add_pill(request):
    itemSeq = request.GET.get("itemSeq","")
    try:
        itemSeq = request.GET.get("itemSeq","")
    except:
        itemSeq = ""
        
    if itemSeq == "":
        return render(request,
                "apuapuapp/add_pill/add_pill.html",
                {})
    else :
        url = url_push(str(itemSeq), 'itemSeq')
        result = response(url)
        items = result['items'][0]
        return render(request,
                    "apuapuapp/add_pill/add_pill.html",
                    {"items":items})

def pill_orc(request):
    file_name = request.GET[file_name]
    # img_file = request.GET[img_file]
    # img_file = img_file.split('\\')
    # file_name = img_file[img_file.length-1]
    # file_name = file_name.split('.')
    # file = file_name[0]
    texts = google_vision_orc("C:/www/apuapuapp/static/apuapuapp/img/"+ file_name)
    # texts = google_vision_orc("C:/www/apuapuapp/static/apuapuapp/img/"+ file +'.jpg')
    return render(request,
                "apuapuapp/add_pill/pill_orc.html",
                # {})
                {"texts": texts})

def popup_search(request):
    now_page = request.GET.get("page","1")
    try:
        now_page = request.GET.get("page","1")
    except:
        now_page = "1"
        
    pill_name = request.GET['pill_name']
    url = url_page(pill_name, 'itemName', now_page)
    result = response(url)
    totalCount = result['totalCount']
    now_page = int(now_page)
    start_page = int((now_page-1)/10)*10 + 1
    if start_page + 9 < int((totalCount-1)/10)+1 :
        end_page = start_page + 9
    else : 
        end_page = int((totalCount-1)/10)+1

    is_prev = False
    is_next = False
    
    if start_page > 1 :
        is_prev = True
    if end_page < int((totalCount-1)/10)+1 :
        is_next = True
    
    return render(request,
                "apuapuapp/add_pill/popup_search.html",
                {"is_prev" : is_prev,
                "is_next" : is_next,
                "start_page" : start_page,
                "page_range" : range(start_page, end_page + 1),
                "result" : result,
                "totalCount" : totalCount,
                "pill_name": pill_name,})

###  복용 리스트  ###
def my_list(request) :
        return render(request,
                    "apuapuapp/my_list.html",
                        {})


###  검색  ###
def seach_list(request) :
    now_page = request.GET.get("page","1")
    try:
        now_page = request.GET.get("page","1")
    except:
        now_page = "1"
        
    keyword = request.GET['keyword']
    search_option =request.GET['search_option']
    url = url_page(keyword, search_option, now_page)
    result = response(url)
    totalCount = result['totalCount']
    if search_option == 'itemName':
        search_option = '약명'
    else : 
        search_option = '제약회사'
    # 한페이지에 보일 행의 갯수
    row = 10 
    now_page = int(now_page)
    start_page = int((now_page-1)/row)*row+1
    if start_page + 9 < int((totalCount-1)/10)+1 :
        end_page = start_page + 9
    else : 
        end_page = int((totalCount-1)/10)+1

    is_prev = False
    is_next = False
    
    if start_page > 1 :
        is_prev = True
    if end_page < int((totalCount-1)/row)+1 :
        is_next = True
    
    return render(request,
                "apuapuapp/search/seach_list.html",
                {"is_prev" : is_prev,
                "is_next" : is_next,
                "start_page" : start_page,
                "page_range" : range(start_page, end_page + 1),
                "result" : result,
                "totalCount" : totalCount,
                "keyword": keyword,
                "search_option" : search_option,
                "now_page" : now_page})

def pill_detail(request) :
    itemSeq = request.GET['itemSeq']
    url = url_push(str(itemSeq), 'itemSeq')
    result = response(url)
    items = result['items'][0]
    
    return render(request,
                "apuapuapp/search/pill_detail.html",
                {'items':items})