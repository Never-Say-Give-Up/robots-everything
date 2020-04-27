#!/usr/bin/env python
# coding: utf-8

# In[14]:
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    import requests
    import re
except:
    print("库不完善，请检查依赖安装情况：")
    print("1. selenium")
    print("2. requests")
    print("3. bs4")
    print("4. re")
    exit(0)
    

#Selenium库 

## initChrome 函数
## 无窗口初始化Chrome模式
## 返回值: (对象)webdriver浏览器
def initChrome():
    oc = Options()
    oc.add_argument('--no-sandbox')  #root模式运行
    oc.add_argument('--headless')  #无窗口模式运行
    try:
        bro = webdriver.Chrome(options=oc)
        return bro
    except:
        print("缺少Chrome驱动，或Chrome安装不正确！")
        exit(0)

        
## getVal函数
## 获取html id属性的文本内容
## 传入值：(对象)浏览器，(字符串)类型<id、name>，(字符串)属性值
## 返回值：(字符串)文本内容
def getVal(bro,types,val):
    if (types == 'id'):
        return str(bro.find_element_by_id(val).text)
    elif (types == 'name'):
        return str(bro.find_element_by_bame(val).text)

#requests库

# *** 基础函数 ***

## getHtml 函数
## 获取网页源代码
## 返回值: (字符串)html源码
def getHtml(htmlurl):
    r = requests.request("GET",htmlurl)
    if (r.status_code != 200):
        print("网络连接错误！")
        exit(0)
    r.encoding = r.apparent_encoding
    return r.text

# *** 基于基础函数的功能函数 ***

## getTitle 函数
## 获取页面标题
## 返回值: (字符串)html标题
def getTitle(text):
    title = re.search('<title>(.+)</title>',text).group()
    title = title.replace("<title>","").replace("</title>","").replace(" ","")
    return title

## getResource 函数
## 获取网页源代码中包含的特定扩展名资源链接
## 返回值: [列表](字符串)资源链接*N
def getResource(text,types):
    return re.findall(r'http://[\S]*' + types,text)

## download 函数
## 下载数据到本地
## 传入值: [列表](字符串)资源url地址 or (字符串)资源url地址
## 返回值: (整型数据)成功(1)、失败(0)
def Download(url,name):
    if (type(url) == list):
        num = 0
        for i in url:
            r = requests.get(i)
            if (r.status_code != 200):
                print("网络连接错误！")
                exit(0)
            with open(str(num) + name,'wb') as file:
                try:
                    num += 1
                    file.write(r.content)
                    print("下载成功！")
                    print("文件名为：" + str(num) + name)
                except:
                    print("文件写入失败！")
                    return 0
        return 1
    elif (type(url) == str):
        r = requests.get(url)
        if (r.status_code != 200):
            print("网络连接错误！")
            exit(0)
        with open(name,'wb') as file:
            try:
                file.write(r.content)
                print("下载成功！")
                print("文件名为：" + name)
                return 1
            except:
                print("文件写入失败！")
                return 0
    
