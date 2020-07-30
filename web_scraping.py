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
import pandas as pd
import os

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

def copy_text(date,month,year,url,dri,memo):
    start1 = time.time()
    rid = url.split("=")[1]
    path = os.getcwd()+"\\"+year+"\\"+month+"\\"+date+"\\"+rid+"\\"
    filepath = year+"\\"+month+"\\"+date+"\\"+rid+"\\"
    Path(path).mkdir(parents=True,exist_ok=True)
    f = open(path+"English.txt","w",encoding="utf-8")
    r = requests.get(url,timeout=100)
    soup = BeautifulSoup(r.text,"html.parser")
    div_text_center = soup.find_all("div",attrs={"class":"text-center"})
    for div in div_text_center:
        if(div.get_text(separator='\r').strip() != ''):
            if 'ReleaseDateSubHeaddateTime' in div.attrs['class']:
                text1 = ' '.join(div.get_text(separator='\r').strip().split())
            else:
                text1 = div.get_text(separator='\r').strip()
            f.write(text1+"\n")
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
    print('wrote english')
    release_lang = soup.find("div",attrs={"class":"ReleaseLang"})
    if(release_lang is None):
        return memo
    a_tags = release_lang.find_all("a")
    print(len(a_tags))
    for i in range(len(a_tags)):
        try:
            print("Starting lang")
            wait = WebDriverWait(dri,200)
            dri.get(url)
            wait.until(presence_of_element_located((By.CLASS_NAME,"ReleaseLang")))
            print("wait done")
            dri.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            main_div = dri.find_elements_by_class_name("ReleaseLang")[0]
            a = main_div.find_elements_by_tag_name("a")[i]
            text_name = a.text
            print('Handling language',text_name)
            key_name = "Parallel1-"+text_name
            a.click()
            wait.until(presence_of_element_located((By.CLASS_NAME,"releaseId")))
            modal = dri.find_elements_by_class_name("ModalWindow")[0]
            print('Finished Modal')
            release_id = modal.find_elements_by_class_name("releaseId")[0].text
            print(release_id)
            releaseId = release_id.split(':')[1].replace(' ','').replace(')','')
            print(releaseId)
            f = open(path+releaseId+"-"+text_name+".txt",'w',encoding="utf-8")
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
            curr_list = [filepath+"English.txt",filepath+releaseId+"-"+text_name+".txt"]
            if(memo.get(key_name) is not None):
                memo[key_name].append(curr_list)
            else:
                memo[key_name] = []
                memo[key_name].append(curr_list)
        except StaleElementReferenceException as e:
            print(e)
        except ElementClickInterceptedException as e:
            print(e)
        except IndexError as e:
            print('Here inner function')
            print(e)
    end1 = time.time()
    print('Time taken for one document for all '+str(len(a_tags))+' languages is ',end1-start1)
    return memo

def select_value(wait,select,value):
    select.select_by_visible_text(value)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    print('Finished selecting',value)

def populate_data(day,month,year,driver,dri):
    start = time.time()
    query_url = "https://www.pib.gov.in/allRel.aspx"
    print('Finished initalize')
    memo = {}
    wait = WebDriverWait(driver,200)
    driver.get(query_url)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    print('Finished loading')
    select_day = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlday")[0])
    if(day != select_day.first_selected_option.text):
        select_value(wait,select_day,day)
    select_day = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlday")[0])
    if(select_day.first_selected_option.text != day):
        return 'Stop'
    select_month = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
    if(month != select_month.first_selected_option.text):
        select_value(wait,select_month,month)
    select_month = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
    if(select_month.first_selected_option.text != month):
        return 'Stop'
    select_year = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlYear")[0])
    if(year!= select_year.first_selected_option.text):
        select_value(wait,select_year,year)
    select_year = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlYear")[0])
    if(select_year.first_selected_option.text != year):
        return 'Stop'
    div = driver.find_elements_by_class_name("content-area")[0]
    div_search = driver.find_elements_by_class_name("search_box_result")[0].text
    print(div_search)
    num = div_search.split(' ')[1]
    num = int(num)
    print(num)
    for i in range(1,num+1):
        try:
            ul = div.find_elements_by_xpath('//*[@id="form1"]/section[2]/div/div[7]/div/div/ul['+str(i)+']')[0]
            li = ul.find_elements_by_tag_name("li")[0]
            ul_leftul = li.find_elements_by_tag_name("ul")[0]
            lis = ul_leftul.find_elements_by_tag_name("li")
            for li_one in lis:
                # li_one = driver.find_elements_by_xpath('//*[@id="form1"]/section[2]/div/div[7]/div/div/ul[3]/li/ul/li[3]')[0]
                a = li_one.find_elements_by_tag_name("a")[0]
                print(a.text)
                print(a.get_attribute("href"))
                memo = copy_text(day,month,year,a.get_attribute("href"),dri,memo)
        except IndexError as e:
            print('Here inside populate_data')
            print(e)
            break
    for key in memo.keys():
        csv_list = memo[key]
        lang = key.split('-')[1]
        header=['English_filename',lang+'_filename']
        df = pd.DataFrame(csv_list)
        filename = month+"-"+key+".csv"
        if(not os.path.exists(filename)):
            df.to_csv(month+"-"+key+".csv",index=False,header=header,mode='a')
        else:
            df.to_csv(month+"-"+key+".csv",index=False,header=False,mode='a')
    end = time.time()
    print('Time taken',end-start)
    return 'Done'


if __name__ == "__main__":
    month = sys.argv[2]
    day = sys.argv[1]
    year = sys.argv[3]
    populate_data(day,month,year)
