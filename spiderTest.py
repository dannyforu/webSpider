from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import time
import json


def getDataFromPage(bsobj, dataSet):
    # bsobj = BeautifulSoup(html.read())
    try:
        # table = bsobj.findAll("td")
        table = bsobj.find("table")
        col = ["xh", "prodNo", "prodName", "manuName", "issueData", "certNo"]
        i = 0;
        for child in table.children:
            try:
                record = child.findAll("td")
                if len(record) != len(col):
                    continue
                j = 0
                recData = {}
                for data1 in record:
                    recData[col[j]] = data1.get_text()
                    j = j + 1
                dataSet.append(recData)
            except Exception as e:
                continue

        # while (i < len(table)):
        #     j = i % len(col)
        #     recData[col[j]] = table[i].get_text()
        #     if j == len(col) - 1:
        #         dataSet.append(recData)
        #         recData = {}
        #     i = i + 1

    except AttributeError as e:
        print(e)


def getNexPage(bsobj):
    url = ''

    linkList = bsobj.findAll("a")
    for link in linkList:
        if link.get_text() == "下一页":
            url = link.attrs["href"]
            return url
    return url


def saveData(fileName, dataSet):
    file = open(fileName, mode="w")
    for data in dataSet:
        jsonData = json.dumps(data, ensure_ascii=False)
        file.write(jsonData + "\n")
    file.close()

def getParam(bsobj, id):
    try:
        t = bsobj.find("input", {"id": id})
        return t.attrs["value"]
    except Exception as e:
        return ""


try:
    html = urlopen("http://www.oscca.gov.cn/app-zxfw/cpxx/symmcp2.jsp")
    bsobj = BeautifulSoup(html.read(), features='html.parser')
    dataSet = []
    getDataFromPage(bsobj, dataSet)
    # 初始化查询参数
    params = {"manuscript_id": "", "curentpage": "", "pagecount": "", "datacount": "", "cpxh": "", "cpmc": "",
              "yzdw": "",
              "xhzsbh": "",
              "starttime": "", "endtime": ""}
    pagecount = getParam(bsobj, "pagecount")
    params["pagecount"] = pagecount

    datacount = getParam(bsobj, "datacount")
    params["datacount"] = datacount

    fileName = "./data.txt"
    # saveData(fileName, dataSet)
    # 寻找下一页
    curentpage = 2

    while (curentpage <= int(pagecount)):
        print("Get Page " + str(curentpage))
        params["curentpage"] = curentpage
        data = urlencode(params).encode('utf-8')
        html = urlopen("http://www.oscca.gov.cn/app-zxfw/cpxx/symmcp2.jsp", data)
        bsobj = BeautifulSoup(html.read(), features='html.parser')
        print("Get Page " + str(curentpage) + "finished")
        getDataFromPage(bsobj, dataSet)
        curentpage = curentpage + 1
        time.sleep(3)

    saveData(fileName, dataSet)

except Exception as e:
    print(e)
