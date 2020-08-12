from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json, base64
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

def send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')

def get_pdf_from_html(path,driver,print_options = {}):
    driver.get(path)
    calculated_print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
	       'preferCSSPageSize': True,
           }
    calculated_print_options.update(print_options)
    result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
    return base64.b64decode(result['data'])
# https://www.pib.gov.in/PressReleasePage.aspx?PRID=1601430
base_url = 'https://www.pib.gov.in/PressReleasePage.aspx?PRID='
driver = get_driver()
list_rid = os.listdir(os.getcwd()+"\\2020\\January\\All")
path = os.getcwd()+"\\2020\\January\\PDF"
for rid in list_rid:
    r = rid.split('-')[0]
    url = base_url+r
    file_name = path+"\\"+rid.split('.')[0]+".pdf"
    # test_file = "testhere.pdf"
    result = get_pdf_from_html(url,driver)
    with open(file_name, 'wb') as file:
        file.write(result)
    print('Done writing '+file_name)
    break
driver.close()
