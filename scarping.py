from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,WebDriverException,ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

def get_driver():
    try:
        executable_path = "C:\\Users\\Dhanvi\\Headless_Browsers\\chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        webdriver1 = webdriver.Chrome(executable_path=executable_path,options=chrome_options)
        return webdriver1
    except WebDriverException as e:
        print(e)
        get_driver()

def copy_text(date,month,year,url,dri):
    start1 = time.time()
    rid = url.split("=")[1]
    path = "C:\\Users\\Dhanvi\\PIB_Scraping"+"\\"+year+"\\"+month+"\\"+date+"\\"+rid+"\\"
    Path(path).mkdir(parents=True,exist_ok=True)
    f = open(path+"English.txt","w",encoding="utf-8")
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    div_text_center = soup.find_all("div",attrs={"class":"text-center"})
    for div in div_text_center:
        if(div.text.strip() != ""):
            text = ' '.join(div.text.split())
            f.write(text+"\n")
    p_tags = soup.find_all("p")
    go_through = len(p_tags)//2
    for p in p_tags[:go_through]:
        if(p.text.strip() != ""):
            text = ' '.join(p.text.split())
            f.write(text+"\n")
    gmail_default = soup.find("div",attrs={"class":"gmail_default"})
    if(gmail_default is not None):
        f.write(gmail_default.text.strip())
    f.close()
    release_lang = soup.find("div",attrs={"class":"ReleaseLang"})
    if(release_lang is None):
        return
    a_tags = release_lang.find_all("a")
    print(len(a_tags))
    for i in range(len(a_tags)):
        try:
            print("Starting lang")
            wait = WebDriverWait(dri,100)
            dri.get(url)
            wait.until(presence_of_element_located((By.CLASS_NAME,"ReleaseLang")))
            print("wait done")
            dri.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            main_div = dri.find_elements_by_class_name("ReleaseLang")[0]
            a = main_div.find_elements_by_tag_name("a")[i]
            text_name = a.text
            print('Handling language',text_name)
            f = open(path+text_name+".txt",'w',encoding="utf-8")
            a.click()
            wait.until(presence_of_element_located((By.CLASS_NAME,"ModalWindow")))
            modal = dri.find_elements_by_class_name("ModalWindow")[0]
            text_center = modal.find_elements_by_class_name("text-center")
            print('Number of text_center',len(text_center))
            for text1 in text_center:
                f.write(text1.text.strip()+"\n")
            p_tags = modal.find_elements_by_tag_name("p")
            print('Number of p_tags',len(p_tags));
            for p in p_tags:
                if(p.text.strip() != ""):
                    f.write(p.text.strip()+"\n")
            pre = modal.find_elements_by_tag_name("pre")
            if(len(pre)>0):
                f.write(pre[0].text.strip()+"\n")
            print("loop done")
            f.close()
        except StaleElementReferenceException as e:
            print(e)
        except ElementClickInterceptedException as e:
            print(e)
    end1 = time.time()
    print('Time taken for one document for all '+str(len(a_tags))+' languages is ',end1-start1)

def select_value(wait,select,value):
    select.select_by_visible_text(value)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    print('Finished selecting',value)

def main(day,month,year):
    start = time.time()
    query_url = "https://www.pib.gov.in/allRel.aspx"
    webdriver1 = get_driver()
    dri = get_driver()
    print('Finished initalize')
    with webdriver1 as driver:
        wait = WebDriverWait(driver,50)
        driver.get(query_url)
        wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
        print('Finished loading')
        select_day = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlday")[0])
        if(day != select_day.first_selected_option):
            select_value(wait,select_day,day)
        select_month = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
        if(month != select_month.first_selected_option):
            select_value(wait,select_month,month)
        select_year = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlYear")[0])
        if(year!= select_year.first_selected_option):
            select_value(wait,select_year,year)
        div = driver.find_elements_by_class_name("content-area")[0]
        div_search = driver.find_elements_by_class_name("search_box_result")[0].text
        num = div_search.split(' ')[1]
        num = int(num)
        for i in range(1,num):
            try:
                ul = div.find_elements_by_xpath('//*[@id="form1"]/section[2]/div/div[7]/div/div/ul['+str(i)+']')[0]
                li = ul.find_elements_by_tag_name("li")[0]
                # ministy_name = li.find_elements_by_class_name("font104")[0].text
                ul_leftul = li.find_elements_by_tag_name("ul")[0]
                lis = ul_leftul.find_elements_by_tag_name("li")
                for li_one in lis:
                    a = li_one.find_elements_by_tag_name("a")[0]
                    print(a.text)
                    print(a.get_attribute("href"))
                    copy_text(day,month,year,a.get_attribute("href"),dri)
            except IndexError as e:
                print(e)
                break
        driver.close()
    dri.close()
    end = time.time()
    print('Time taken',end-start)


if __name__ == "__main__":
    month = sys.argv[2]
    day = sys.argv[1]
    year = sys.argv[3]
    main(day,month,year)
