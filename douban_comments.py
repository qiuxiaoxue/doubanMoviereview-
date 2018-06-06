#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import xlwt
import sys
from util import get_HTMLText
import importlib
importlib.reload(sys)

#获取相关内容
def getData(baseurl):
    #1 找到评论标题
    pattern_title = re.compile(r'<a class="subject-img" title="(.+)"')
    #2 找到评论全文链接
    pattern_link = re.compile(r'<div class="main-bd"> <h2>a href="(.+review.*?)"')
    #找到作者
    # pattern_author = re.compile(r'<a.+people.+">(.+)</a>')
    #3 找到评论的影片和影评详情链接
    pattern_subject_link = re.compile(r'<a class="(.+subject.+)" href="(.+)">')
    #4 找到推荐等级
    pattern_star=re.compile(r'<a class="action-btn down" title="(.+)"></a>')
    #5 找到回应数
    pattern_response=re.compile(r'<a class="reply">\((\d+)回应\)</a>')
    #6 找到有用数
    pattern_use=re.compile(r'<button class="btn.+"> \(有用(\d+)\)</button>')
    remove=re.compile(r'<.+?>')#去除标签
    datalist=[]

    for i in range(0,5):#总共5页
        url=baseurl+str(i*10)#更新url
        html = get_HTMLText(url)
        print(url + ":" +html)
        soup = BeautifulSoup(html,"lxml")
        #找到每一个影评项
        for item in soup.find_all('div',typeof='v:Review'):
            data=[]
            item=str(item)#转换成字符串
            #print item
            title = re.findall(pattern_title,item)[0]
            #print title
            reviewlink=re.findall(pattern_link,item)[0]
            data.append(title)#添加标题
            #author=re.findall(pattern_author, item)[0]
            #data.append(author)#添加作者
            list_subject_link = re.findall(pattern_subject_link, item)[0]
            moviename=list_subject_link[1]
            movielink=list_subject_link[0]
            data.append(moviename)#添加片名
            data.append(movielink)#添加影片链接
            star=re.findall(pattern_star,item)[0]
            data.append(star)#添加推荐等级
            response=re.findall(pattern_response,item)
            #回应数可能为0，就找不到
            if(len(response)!=0):
                response=response[0]
            else:
                response=0
            data.append(response)#添加回应数
            data.append(reviewlink)#添加评论正文链接
            content = get_HTMLText(reviewlink)
            use=re.findall(pattern_use,content)
            #有用数可能为0，就找不到
            if len(use)!=0:
                use=use[0]
            else:
                use=0
            content=BeautifulSoup(content)
            desc=content.find_all('div',id='link-report')[0]
            desc=re.sub(remove,'',str(desc))#去掉标签
            data.append(desc)#添加评论正文
            data.append(use)#添加有用数
            datalist.append(data)
    return datalist

#将相关数据写入excel中
def saveData(datalist,savepath):
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('豆瓣最受欢迎影评',cell_overwrite_ok=True)
    col=('标题','影片名','影片详情链接','推荐级','回应数','影评链接','影评','有用数')
    for i in range(0,9):
        sheet.write(0,i,col[i])#列名
    for i in range(0,10):#总共50条影评
        data=datalist[i]
        for j in range(0,9):
            sheet.write(i+1,j,data[j])#数据
    book.save(savepath)#保存

def main():
    baseurl='http://movie.douban.com/review/best/?start='
    datalist=getData(baseurl)
    savapath=u'豆瓣最受欢迎影评.xlsx'
    saveData(datalist,savapath)

main()