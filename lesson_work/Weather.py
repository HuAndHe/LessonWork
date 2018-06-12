# -*- coding=utf-8 -*-
#用命令行打开文件会报错，麻烦用PyCharm打开运行此文件。
from bs4 import BeautifulSoup
import requests
import xlwt
import os

#获得某一个月的天气数据
def getListByUrl(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    weathers = soup.select("#tool_site")
    title = weathers[1].select("h3")[0].text
    weatherInfors = weathers[1].select("ul")
    weatherList = list()
    for weatherInfor in weatherInfors:
        singleWeather = list()
        for li in weatherInfor.select('li'):
            singleWeather.append(li.text)
        weatherList.append(singleWeather)
    print(title)
    return weatherList,title

#@par:addressUrl 获得某地区的数据
#@par:excelSavePath  数据的保存地址
def getListByAddress(addressUrl,excelSavePath):
    # url = "http://lishi.tianqi.com/beijing/index.html"
    url = addressUrl
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    dates = soup.select(".tqtongji1 ul li a")
    workbook = xlwt.Workbook(encoding='utf-8')
    for d in dates:
        weatherList,title = getListByUrl(d["href"])
        booksheet = workbook.add_sheet(title,cell_overwrite_ok=True)
        for i,row in enumerate(weatherList):
            for j,col in enumerate(row):
                booksheet.write(i,j,col)
    workbook.save(excelSavePath)


if __name__ == "__main__":
    addressName = raw_input("请输入即将获取天气的城市:\n")
    addresses = BeautifulSoup(requests.get('http://lishi.tianqi.com/').text,"html.parser")
    queryAddress = addresses.find_all('a',text=addressName)
    if len(queryAddress):
		#这里必须在C盘下新建一个Table文件夹，否则保存不了数据。
        savePath = raw_input("检测到有该城市数据，请输入即将保存天气数据的路径（如若不输入，将默认保存到c:/Table/"+addressName+".xls）:\n")
        if not savePath.strip():
            if not os.path.exists('c:/Table'):
                os.makedirs('c:/Table')
            savePath = "c:/Table/"+addressName+".xls"
        for q in queryAddress:
            getListByAddress(q["href"],savePath)
            print("已经天气数据保存到:"+savePath)
    else:
        print("不存在该城市的数据")