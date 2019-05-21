from urllib.request import urlopen
from bs4 import BeautifulSoup


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


html = urlopen("http://www.oscca.gov.cn/app-zxfw/cpxx/symmcp2.jsp")
bsobj = BeautifulSoup(html.read())
dataSet = []
getDataFromPage(bsobj, dataSet)
# 寻找下一页
url = getNexPage(bsobj)
for data in dataSet:
    print(data)
