from urllib.parse import urlencode, unquote, quote_plus
import requests
import xml
import json
import urllib.request
from bs4 import BeautifulSoup

key = "sBYkI2dLvtnNLK%2FqW492rbtS%2Fd8Zju2vCUMwyMZleunbV8piPNH1jfvjyjBps0WmoQ00uOEbcsN9T6v5I%2BxHcg%3D%3D"

url = f'https://api.odcloud.kr/api/15077669/v1/uddi:09c1cd67-579b-40fd-8578-de96b733370f?page=1&perPage=675&returnType=JSON&serviceKey={key}'


def get_WasteMedicine_dict():
    r = urllib.request.urlopen(url)

    # 데이터를 json형태로 받아오기
    data = json.loads(r.read())

    result = {}
        
    for i in range(data['currentCount']):
        reg_no = data['data'][i]['연번']
        sigungu = data['data'][i]['시군구']
        pharmacy = data['data'][i]['약국명']
        phone_number = data['data'][i]['전화번호']
        address = data['data'][i]['소재지']
    
        info = {
                '연번': reg_no,
                '시군구': sigungu,
                '약국명': pharmacy,
                '전화번호': phone_number,
                '소재지': address
        }
        
        result[i+1] = info
    
    
    return result
    


def get_city_list(city_list, res):
    selected_lists = []
    result = {}

    for key, value in res.items():
        if value["시군구"] in city_list:
            selected_lists.append(value)

    for i in range(len(selected_lists)):
        reg_no = i + 1
        sigungu = selected_lists[i]["시군구"]
        pharmacy = selected_lists[i]["약국명"]
        phone_number = selected_lists[i]["전화번호"]
        address = selected_lists[i]["소재지"]

        info = {
            "연번": reg_no,
            "시군구": sigungu,
            "약국명": pharmacy,
            "전화번호": phone_number,
            "소재지": address,
        }

        result[i + 1] = info

    return result
    

