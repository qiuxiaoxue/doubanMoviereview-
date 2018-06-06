#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import xlwt
import sys
from util import get_HTMLText
import importlib
import pandas as pd
import time
import random
importlib.reload(sys)


def getData(baseurl):
    # scrapy_short_criticism(baseurl)
    scrapy_long_criticism(baseurl)

def scrapy_short_criticism(baseurl):
    for i in range(0,5):#总共5页
        url = baseurl+str(i*10)#更新url
        html = get_HTMLText(url)
        soup = BeautifulSoup(html,"lxml")
        #找到最受欢迎的影评页每一个影评项
        for item in soup.find_all('div',typeof='v:Review'):
            data = []
            item = str(item)#转换成字符串
            item = BeautifulSoup(item , "lxml")

            movie_name_list = getMovie_record('short')
            title = item.img['alt'] #获取影片名
            if title in movie_name_list:
                continue
            else:
                movieRecord_add(title,'short')
            movie_link = item.div.a['href']#获取影片链接
            One_movie_html = get_HTMLText(movie_link)
            #获取每部电影评论总和页面
            One_movie_soup = BeautifulSoup(One_movie_html,"lxml")
            #获取这部电影的短评总数
            criticismSum = One_movie_soup.find_all('div',class_="mod-hd")
            criticismSum = str(criticismSum)#转换成字符串
            criticismSum = BeautifulSoup(criticismSum,"lxml")
            criticismSum = criticismSum.find_all('a')
            # IP是否被封而查询不到网页
            try:
                criticismSum = int(criticismSum[1].text.strip().split(" ")[1])
            except:
                print("IP已被查封。。。")
                savef(data, str(title)+"短评")
                sys.exit(0)

            for i in range(0,int(criticismSum),20):#每页只能显示20条评论循环遍历
                One_movie_html = get_HTMLText(movie_link + "/comments?start="+str(i))
                # 获取当前页bs4soup
                One_movie_html = BeautifulSoup(One_movie_html,"lxml")
                try:
                    #获取每页20条评论
                    criticismContent = One_movie_html.find_all("div",class_="comment")
                    criticismName = One_movie_html.find_all("span",class_="comment-info")
                    # criticismStar = criticismName
                    criticismGood = One_movie_html.find_all("span",class_="votes")
                except:
                    print("抓取单页评论时出错。。。")
                    print("当前评论网页地址为：" + movie_link + "/comments?start=" + str(i))
                    break
                #开始抓取每行评论
                for j in range(0,19):
                    datasmall = []
                    try:
                        datasmall.append(title)  # 1 添加电影名
                        datasmall.append(criticismContent[j].p.text.strip())  # 2 添加电影评论内容
                        datasmall.append(criticismName[j].a.text.strip())  # 3 添加电影评论人名

                        criticismStar = str(criticismName[j])  # 转换成字符串
                        criticismStar = BeautifulSoup(criticismStar, "lxml")
                        criticismStar = criticismStar.find_all('span')
                        criticismStar = criticismStar[2]['title']
                        datasmall.append(criticismStar) # 4 添加电影推荐星数
                        datasmall.append(criticismGood[j].text.strip())  # 5 添加电影有用数
                    except:
                        break
                    data.append(datasmall)
                # print("抓取单页评论时出错。。。")
                time.sleep(random.randint(5,10))
            print(title+"评论数据抓取完成，正在存写入。。。")
            #每一页的评论进行写一次
            savef(data, str(title)+"短评")
            print(title + "评论数据抓取存写完成。")

def scrapy_long_criticism(baseurl):
    for i in range(0,5):#总共5页
        url = baseurl+str(i*10)#更新url
        html = get_HTMLText(url)
        soup = BeautifulSoup(html,"lxml")
        #找到最受欢迎的影评页每一个影评项
        for item in soup.find_all('div',typeof='v:Review'):
            data = []
            movie_name_list = getMovie_record('long')
            print(movie_name_list)
            item = str(item)#转换成字符串
            item = BeautifulSoup(item, "lxml")
            #每部影评第一条评论的详细链接
            # reviewlink = item.h2.a['href']

            title = item.img['alt'] #获取影片名
            if title in movie_name_list:
                continue
            else:
                movieRecord_add(title,'long')
            print(title)
            movie_link = item.div.a['href']#获取影片链接
            # print(movie_link)
            One_movie_html = get_HTMLText(movie_link)
            #获取每部电影评论总和页面
            One_movie_soup = BeautifulSoup(One_movie_html,"lxml")
            #获取这部电影的评论总数
            criticismSum = One_movie_soup.find_all('div',class_="mod-hd")
            criticismSum = str(criticismSum)#转换成字符串
            criticismSum = BeautifulSoup(criticismSum,"lxml")
            criticismSum = criticismSum.find_all('a')
            # IP是否被封而查询不到网页
            try:
                criticismSum = int(criticismSum[1].text.strip().split(" ")[1])
            except:
                print("IP已被查封。。。")
                sys.exit(0)
            for i in range(0,int(criticismSum),20):#每页只能显示20条评论循环遍历
                One_movie_html = get_HTMLText(movie_link + "/reviews?start="+str(i))
                # 获取当前页bs4soup
                One_movie_html = BeautifulSoup(One_movie_html,"lxml")
                #获取每页20条评论
                criticismContent = One_movie_html.find_all("div",class_="short-content")
                criticismName = One_movie_html.find_all("a",class_="name")
                criticismStar = One_movie_html.find_all("span",property="v:rating")
                criticismGood = One_movie_html.find_all("a",class_="action-btn up")

                for j in range(0,19):
                    datasmall = []
                    #本页评论没有20条
                    if(len(criticismContent)<20):
                        break
                    datasmall.append(title)  # 1 添加电影名
                    datasmall.append(criticismContent[j].text.strip())  # 2 添加电影评论内容
                    datasmall.append(criticismName[j].text.strip())  # 3 添加电影评论人名
                    if(j > (len(criticismStar)-2)):
                        break
                    datasmall.append(criticismStar[j]['title'])  # 4 添加电影推荐星数
                    datasmall.append(criticismGood[j].span.text.strip())  # 5 添加电影有用数
                    data.append(datasmall)
                    print(title + "评论数据抓取中。。。")
            time.sleep(random.randint(3,5))
            #每一页的评论进行写一次
            savef(data, str(title))

def movieRecord_add(movie_name,kind):
    #按行追加写入
    if kind == 'long' :
        with open('scrapied_movie.txt', 'a',encoding='UTF-8') as file_object:
            file_object.write('\n'+movie_name)
    else:
        with open('scrapied_movie_short.txt', 'a', encoding='UTF-8') as file_object:
            file_object.write('\n' + movie_name)

def getMovie_record(kind):
    movie_record = []
    if kind == 'long':
        file = open('scrapied_movie.txt', 'r', encoding='UTF-8', errors='ignore')
    else:
        file = open('scrapied_movie_short.txt', 'r', encoding='UTF-8', errors='ignore')
    for line in file.readlines():#一次读取文件的全部内容，并按行返回list
        movie_record.append(line.replace('\n',''))
    return movie_record

def savef(datalist, filename):
	col=('影片名','评论内容','评论人','推荐星数','有用数')
	df = pd.DataFrame(datalist,columns=col)
	print(filename)
	df.to_csv(filename.replace('：',"")+'.csv')

#将相关数据写入excel中
def saveData(datalist,savepath):
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('豆瓣最受欢迎影评',cell_overwrite_ok=True)
    col=('影片名','评论内容','评论人','推荐星数','有用数')
    for i in range(0,5):
        sheet.write(0,i,col[i])#列名

    for i in range(0,10):#总共50条影评
        data1 = datalist[i]
        # print(type(data))
        for j in range(0,5):
            sheet.write(i+1,j,data1[j])#数据
    book.save(savepath)#保存

def main():
    baseurl='http://movie.douban.com/review/best/?start='
    getData(baseurl)

main()