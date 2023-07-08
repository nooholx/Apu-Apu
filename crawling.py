import json
import time
import re
import os
import requests
import datetime
import locale
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import pymysql
import my_settings


locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from boardapp.models import Board


id = my_settings.id
pw = my_settings.pw


regNo_list = []
title_list = []
date_list = []
link_list = []
content_list = []

result = []



# 크롤링 결과값 dict로 저장
def get_boardDict(result):
    
    for i in range(len(regNo_list)):

        temp_dict = {
            'b_no': regNo_list[i],
            'b_title': title_list[i],
            'b_note': content_list[i],
            'b_writer': 'admin',
            'b_date': date_list[i],
            'b_link' : link_list[i]
        }

        result.append(temp_dict)
    return result


# 글 내용 크롤링 함수
def get_content(content_list):
    # 1. id/pw입력 후에 로그인 버튼 클릭하게 하기
    url = 'https://www.health.kr/main.asp'

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    # time.sleep(2)

    driver.find_element(By.ID, 'id').send_keys(id)
    driver.find_element(By.ID, 'passwd').send_keys(pw)
    submit = driver.find_element(By.XPATH, '//*[@id="login"]/button')
    submit.click()

    # 2. 공지사항 클릭하기
    driver.find_element(By.XPATH, '//*[@id="nav_cont"]/ul/li[8]/a').click()

    # 3. 페이지 리스트만큼 크롤링하기
    #    게시글 하나하나 눌러서 내용 크롤링하고 뒤로가기
    page = 1
    page2 = 1
    error_cnt = 0

    while True:
        print("**", page, "**")

        # 페이지 넘어가며 출력
        try:
            # 페이지 번호 클릭 전에 해당 번호의 요소가 있는지 확인
            page_xpath = f'//*[@id="paging"]/span/a[{page2}]'
            page_elements = driver.find_elements(By.XPATH, page_xpath)
            # print(page_elements)

            if not page_elements:
                break
            page_elements[0].click()


            # 게시글 리스트 내용 크롤링
            write_list = driver.find_elements(By.CSS_SELECTOR, '.txtL')


            for write in write_list:
                # print(write.text)
                # 게시글 클릭
                link = write.find_element(By.TAG_NAME, 'a')
                link.click()

                # 게시글 내용 크롤링
                content = driver.find_element(By.CSS_SELECTOR, '.cont').text
                content_list.append(content)

                # 뒤로가기
                driver.back()

                # 잠시 대기
                time.sleep(1)

            page += 1
            page2 += 1
            error_cnt = 0


        except Exception as e:
            error_cnt += 1
            print("Error occurred:", str(e))

            # 오류가 3번 연속 발생하면 크롤링 종료
            if error_cnt >= 3:
                break

    driver.quit()


# 
def get_boardInfo(requests, regNo_list, title_list, date_list, link_list ):
    
    # 마지막 페이지 번호 찾기
    max_page = get_maxPage()

    # 페이지별 게시글 정보 크롤링하기
    for i in range(1, max_page+1):
        url = 'https://www.health.kr/notice/safety.asp?'
        params = {
            'inputField': '',
            'search_term': '',
            'paging_value': i,
            'setLine': '',
            'setHeader': ''
        }
        response = requests.get(url, params=params)

        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        elements = soup.select('tr')

        for e in elements[1:]:
            td_elements = e.find_all('td')

            if len(td_elements) >= 4:
                regNo = td_elements[0].text.strip()
                regNo_list.append(regNo)

                title = td_elements[1].text.replace('\n', '').strip()
                title_list.append(title)

                date = td_elements[3].text.strip()
                date_list.append(date)

            link = e.find('a')['href']
            link_list.append('https://www.health.kr/notice/' + link)
    


# 마지막 페이지 번호 찾는 함수
def get_maxPage():
    url = 'https://www.health.kr/notice/safety.asp'
    response = requests.get(url)
    
    # 한글 깨질 경우 
    html = response.content.decode('utf-8', 'replace')
    soup = BeautifulSoup(html, 'lxml')

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    # 페이지 번호 요소 추출
    page_elements = driver.find_elements(By.CSS_SELECTOR, '#paging span a') 
        
    # 페이지 번호 요소 추출
    page_elements = driver.find_elements(By.CSS_SELECTOR, '#paging span a')

    # 추출한 페이지 번호를 숫자로 변환하여 가장 큰 값 찾기
    max_page = 0
    for element in page_elements:
        page_text = element.text.strip()
        if page_text.isdigit():  # 숫자인지 확인
            page_number = int(page_text)  # 페이지 번호를 숫자로 변환
            if page_number > max_page:
                max_page = page_number
                
    # Selenium 웹 드라이버 종료
    driver.quit()
    
    return max_page


get_maxPage()
get_boardInfo(requests, regNo_list, title_list, date_list, link_list)
get_content(content_list)
get_boardDict(result)



# insert data into sqlite
if __name__=='__main__':
    board_data = get_boardDict(result)
    for item in board_data:
        Board(b_no = item['b_no'], 
            b_title = item['b_title'], 
            b_note = item['b_note'],
            b_writer = item['b_writer'],
            b_date = item['b_date'],
            b_link = item['b_link']).save()
