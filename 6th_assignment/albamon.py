#알바몬에서 키워드 검색 후 구인광고 지역, 제목, 급여 정보 추출

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time
import csv

path = os.getcwd() + "\chromedriver.exe"
driver = webdriver.Chrome(path)

try : 
    driver.get("https://www.albamon.com/?la_gc=CN3B330392286&la_src=sa&la_cnfg=2589421&gclid=Cj0KCQjwy6T1BRDXARIsAIqCTXq_KdIkUOwLyc1u04014NJr9wbOITa-VonU4KECzkIDPHdUPhT5kUkaAqYbEALw_wcB")
    time.sleep(3)

    searchIndex = "카페 알바"
    element = driver.find_element_by_class_name("sm")
    element.send_keys(searchIndex)
    driver.find_element_by_id("btn_searchKeyword").click()

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    
    page =[]
    local = []
    title =[]
    pay =[]

    for i in range(10) :    
        time.sleep(1)
        
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        conts = bs.find("div", class_ = "smResult").find_all("div", class_ = "booth")
        
        local.append("page" + str(i+1))
        title.append(" ")
        pay.append(" ")

        for c in conts :
            local.append(c.find("dd", class_ = "local").text)
            title.append(c.find('a').text)
            pay.append(c.find("dd", class_ = "etc").find("span").text)
      
        page = driver.find_element_by_class_name("listPaging").find_elements_by_tag_name('a')
        page[i].click()  #다음 페이지로 넘어가는 버튼이 10페이지씩 넘기는 것 밖에 없고, url주소는 복잡해서 페이지 버튼들을 리스트로 받아서 순서대로 클릭하도록 함.

finally :
    for i in range(len(local)):
        if local[i].find("page") != -1 :
            print()
            print(local[i])
        else :
            print("지역 : " + local[i] + "제목 : " + title[i] + " 급여 : " + pay[i])
    driver.quit()