import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_chrome(url,hide=False):
    try:
        options = webdriver.ChromeOptions()
        if hide :
            options.add_argument('--headless')
        chrome = webdriver.Chrome(options = options)
        chrome.get(url)
        return chrome
    except Exception as e:
        print(e)

def getSoup(url,post_data=None):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    try:
        if post_data is not None:
            resp = requests.post(url,post_data,headers=headers)
        else:
            resp = requests.get(url,headers=headers)
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text,'lxml')
            return soup
        else:
            print('網頁取得失敗')
    except Exception as e:
        print('網址錯誤',e)

def get_date(hms=False):
    now = datetime.now().strftime('%Y-%m-%D')

def save_pic(url,fileName = 'temp.jpg'):
    try:
        resp = requests.get(url)
        if resp.status_code ==200:
            with open(f'{fileName}','wb') as f:
                f.write(resp.content)
                print(f'{fileName}儲存成功')
    except Exception as e:
        print('儲存失敗',resp.status_code,e)

def make_dirs(path):
    '''
        建立目錄路徑
    '''
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'{path}建立成功')
        else:
            print(f'{path}已經存在')
    except Exception as e:
        print(e)

def scroll_window(chrome,start=0,end=10000,step=500,delay_time=0.5):
    while start <=end :
        print(start)
        chrome.execute_script(f'window.scrollTo({start},{start+step})')
        start+=step
        time.sleep(delay_time)

        
def find_element(chrome,xpath):
    try:
        return chrome.find_element(By.XPATH,xpath)
    except Exception as e:
        print(e)





if __name__=='__main__':
    # make_dirs('temp/12345')
    url = 'http://www.yahoo.com.tw'
    api_url = 'https://www.ibon.com.tw/retail_inquiry_ajax.aspx'
    form_data = {
        'strTargetField': 'COUNTY',
        'strKeyWords': '台中市'
    }
    print(getSoup(api_url,form_data))

    chrome = get_chrome(url,hide=True)
    if chrome is not None:
        chrome.quit()
        print('關閉成功')

    # print(getSoup(url))