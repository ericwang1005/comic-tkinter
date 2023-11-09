from tools import get_chrome, getSoup
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as message
import requests
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread


font1 = ("微軟正黑體", 36)
font2 = ("標楷體", 42)
font3 = ("標楷體", 16)
size = '720x360'


def create_app(size='400x300', title='EW_Asset_System', shrink=False):
    app = tk.Tk()
    if size == None:
        app.geometry(size)
    app.title(title)
    app.resizable(shrink, shrink)
    return app


def update_btn():
    keys = entry.get()
    thread = Thread(target=search_comic, args=(keys,))
    thread.start()  # 使用start() 啟動線程
    if thread.is_alive():
        read_btn.config(state='normal', fg='black')
        label2.config(text='查詢完畢!', fg='green')
        showinfo_btn.config(state='normal', fg='black')
        clear_btn.config(state='normal', fg='black')


def search_comic(keys):
    datas = []
    try:
        url = 'https://www.manhuaren.com/search/'
        chrome = get_chrome(url, hide=True)
        search_xpath = '/html/body/div[1]/div/input'
        element = chrome.find_element(By.XPATH, search_xpath)
        element.clear()
        time.sleep(1)
        element.send_keys(f'{keys}')
        time.sleep(1)
        element.send_keys(Keys.RETURN)
        confirm_xpath = '/html/body/div[1]/a[2]'
        chrome.find_element(By.XPATH, confirm_xpath).click()
        soup = BeautifulSoup(chrome.page_source, 'lxml')
        comic_list = soup.find('ul', class_="book-list").find_all('li')
        for comic in comic_list:
            link = 'https://www.manhuaren.com' + \
                comic.find('a').get('href')
            title = comic.find('a').get('title')
            info = comic.find('p', class_='book-list-info-desc').text.strip()
            img_url = comic.find('img').get('src')
            datas.append([title, link, info, img_url])

        df = pd.DataFrame(datas, columns=['Title', 'Link', 'Info', 'Img_url'])
        for row in df.itertuples(index=False):
            list_field.insert(tk.END, row)

    except Exception as e:
        print(e)
    finally:
        chrome.quit()


def read_comic():
    select = list_field.curselection()
    if select != ():
        index = select[0]
        data = list_field.get(index)
        webbrowser.open(data[1])


def show():
    select = list_field.curselection()
    if select != ():
        index = select[0]
        data = list_field.get(index)
        label3.config(text=data[0])
        label4.config(text=data[2])
        try:
            resp = requests.get(data[-1])
            if resp.status_code == 200:
                img_data = BytesIO(resp.content)
                img = Image.open(img_data)
                photo = ImageTk.PhotoImage(img)
                image_label = ttk.Label(
                    app_frame2, image=photo)
                image_label.photo = photo
                image_label.grid(row=2, column=0, sticky='nsew')
                style = ttk.Style()
                style.configure('image_label', background='ivory3')
        except Exception as e:
            print(e)


def clear_result():
    if list_field.size() > 0:
        list_field.delete(0, 'end')
        entry.delete(0, 'end')


app = create_app(size=size, title='Comic App', shrink=True)
list_var = tk.StringVar()
list_var.set([])
app_frame = tk.Frame(app, bg='ivory2')
app_frame.pack(fill='both')
app_frame2 = tk.Frame(app, bg='ivory3')
app_frame2.pack(fill='both')
label1 = tk.Label(app_frame, text='Comic App', font=font2,
                  fg='black').grid(row=0, column=0)
label2 = tk.Label(app_frame, text='查找狀態', font=font1,
                  fg='black')
label2.grid(row=1, column=3)
label3 = tk.Label(app_frame2, text='', font=font1, fg='black', bg='ivory3')
label3.grid(row=0, column=0, sticky='w')
label4 = tk.Label(app_frame2, text='', font=font3, fg='black', bg='ivory3')
label4.grid(row=1, column=0, sticky='nsew')
entry = tk.Entry(app_frame)
entry.grid(row=0, column=5)
search_btn = tk.Button(app_frame, text='Search',
                       command=update_btn).grid(row=0, column=6)
read_btn = tk.Button(app_frame, text='Read Comic',
                     command=read_comic)
read_btn.grid(row=0, column=7)
read_btn.config(state='disabled')
# 放入 Button，設定 command 參數
showinfo_btn = tk.Button(app_frame, text='顯示資訊',
                         command=show)
showinfo_btn.grid(row=3, column=0)
showinfo_btn.config(state='disabled')
clear_btn = tk.Button(app_frame, text='清除紀錄',
                      command=clear_result)
clear_btn.grid(row=3, column=1)
clear_btn.config(state='disabled')
list_field = tk.Listbox(app_frame,
                        font=font3, fg='black', width=30)
list_field.grid(row=1, column=0)

app.mainloop()
