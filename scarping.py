from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located

query_url = "https://www.pib.gov.in/allRel.aspx"

month = "June"
day = "All"
year = "2020"

executable_path = "C:\\Users\\Dhanvi\\Headless_Browsers\\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")
webdriver1 = webdriver.Chrome(executable_path=executable_path,options=chrome_options)
print('Finished initalize')

def select_month(wait,select,value):
    select.select_by_visible_text(value)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    div = driver.find_elements_by_class_name("content-area")[0]
    return div


with webdriver1 as driver:
    wait = WebDriverWait(driver,20)
    driver.get(query_url)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    select = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
    div = select_month(wait,select,month)
    uls = div.find_elements_by_tag_name("ul")
    for ul in uls[1:3]:
        for a in ul.find_elements_by_tag_name("a"):
            print(a.text)
            print(a.get_attribute("href"))
    print(len(uls))
    print("Finished waiting")
