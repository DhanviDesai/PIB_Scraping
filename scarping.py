from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import sys
import requests
from bs4 import BeautifulSoup

def get_driver():
    executable_path = "C:\\Users\\Dhanvi\\Headless_Browsers\\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    webdriver1 = webdriver.Chrome(executable_path=executable_path,options=chrome_options)
    return webdriver1

def print_data(url,index):
    webdriver1 = get_driver()
    with webdriver1 as driver:
        wait = WebDriverWait(driver,20)
        driver.get(url)
        wait.until(presence_of_element_located((By.CLASS_NAME,"ReleaseLang")))
        main_div = driver.find_elements_by_class_name("ReleaseLang")[0]
        a = main_div.find_elements_by_tag_name("a")[index]
        a.click()
        main_div_modal = driver.find_elements_by_class_name("ModalWindow")[0]
        div_text_center = main_div_modal.find_elements_by_class_name("text-center")
        for text_center in div_text_center:
            print(text_center.text.strip())
        p_tags = main_div_modal.find_elements_by_tag_name("p")
        for p in p_tags:
            print(p.text.strip())


def copy_text(name,url):
    try:
        f = open(name+".txt","w")
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
        f.close()
        release_lang = soup.find("div",attrs={"class":"ReleaseLang"})
        a_tags = release_lang.find_all("a")
        print(len(a_tags))
        for i in range(len(a_tags)):
            print("Starting lang")
            webdriver2 = get_driver()
            with webdriver2 as dri:
                wait = WebDriverWait(dri,20)
                dri.get(url)
                wait.until(presence_of_element_located((By.CLASS_NAME,"ReleaseLang")))
                print("wait done")
                main_div = dri.find_elements_by_class_name("ReleaseLang")[0]
                a = main_div.find_elements_by_tag_name("a")[i]
                f = open(name+""+a.text+".txt",'w',encoding="utf-8")
                a.click()
                wait.until(presence_of_element_located((By.CLASS_NAME,"ModalWindow")))
                modal = dri.find_elements_by_class_name("ModalWindow")[0]
                text_center = modal.find_elements_by_class_name("text-center")
                for text1 in text_center:
                    f.write(text1.text.strip()+"\n")
                p_tags = modal.find_elements_by_tag_name("p")
                for p in p_tags:
                    f.write(p.text.strip()+"\n")
                print("loop done")
                f.close()
    except AttributeError as a:
        print('In error')
        print(a)

def select_value(wait,select,value):
    select.select_by_visible_text(value)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    print('Finished selecting')

def main():
    query_url = "https://www.pib.gov.in/allRel.aspx"
    month = sys.argv[2]
    day = sys.argv[1]
    year = sys.argv[3]
    webdriver1 = get_driver()
    print('Finished initalize')
    with webdriver1 as driver:
        wait = WebDriverWait(driver,30)
        driver.get(query_url)
        wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
        select_day = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlday")[0])
        select_value(wait,select_day,day)
        select_month = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
        select_value(wait,select_month,month)
        select_year = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlYear")[0])
        select_value(wait,select_year,year)
        div = driver.find_elements_by_class_name("content-area")[0]
        uls = div.find_elements_by_tag_name("ul")
        for ul in uls[1:2]:
            for a in ul.find_elements_by_tag_name("a"):
                print(a.text)
                print(a.get_attribute("href"))
                copy_text(a.text,a.get_attribute("href"))

        # print(len(uls))
        print("Finished waiting")

if __name__ == "__main__":
    main()
