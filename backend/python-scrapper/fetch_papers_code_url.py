# [code, url]
allPapers = list()
# [url]
crawled = set()
# [code] [branch][code]
codes = dict()

branches = ["BA","BC","BD","BE","BESP","BH","BI","BL","BM","BP","BPSP","BT","BV","DA","DI","DISP","DP","DV","FD","HM","IC","MA","MB","MC","MCSP","ME","ML","MN","MP","MR","MT","PD","PH","PM","PP","PR","TE","VM"]

from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
import requests
from pathlib import Path
import time
import json


def savePaperJson():
    global allPapers
    # convert the list to JSON!
    papers_json = json.dumps(allPapers)

    # Write out the list to file.
    file = open("./papers.json", "w+")
    file.write(papers_json)
    file.close()

def page(url, check=False):
    global allPapers
    # check if site is indeed an PDF Or Zip
    status_code = 200
    content_type = "pdf"
    if(check):
        res = requests.head(url)
        status_code = res.status_code
        content_type = res.headers["Content-Type"]

    if ((not content_type.__contains__("html")  and status_code < 400) and (url.endswith(".zip") or url.endswith(".pdf"))):
        t2 = url.split("/")
        t2 = t2[t2.__len__() - 1]

        code = t2.split(".")[0]
        for branch in branches:
            if url.__contains__(branch):
                if not codes.__contains__(branch):
                    codes[branch] = list()
                codes[branch].append(code)

        curPaper = [code, url]

        allPapers.append(curPaper)
        # print("Added", curPaper)
        return True
    else:
        print("File at", url, "is not pdf or zip!")
        rec(url)
        return False


def rec(baseURL):
    basePage = requests.get(baseURL).text
    aTags = bs(basePage, "html.parser").find_all("a")
    for a in aTags:
        hreflink = urljoin(baseURL,a.get("href"))
        valid = ((
            hreflink.startswith("http://www.gtu.ac.in")) or (hreflink.startswith(
        "http://old.gtu.ac.in")) or (hreflink.startswith("http://files.gtu.ac.in")))
        if((hreflink == "http://www.gtu.ac.in") or (hreflink == "http://gtu.ac.in/Download1.aspx") or (hreflink == "http://www.gtu.ac.in/")):
            continue
        else:
            if valid:
                if(not crawled.__contains__(hreflink)):
                    crawled.add(hreflink)
                    page(hreflink)
            else:
                print("Link not in crawling domain!", hreflink)

# recursively got for all the papers!            
base = "http://old.gtu.ac.in/Qpaper.html"
rec(base)
savePaperJson()

# Add all new papers [W2017-W2019]
base =  "https://www.gtu.ac.in/uploads"
sems = ["W2019","S2018","W2018","S2019", "W2017"]
prefix = dict()
for branch in branches:
  prefix[branch] = []

for sem in sems:
    for branch in branches:
        for code in codes[branch]:
          if code[:3] not in prefix[branch]:
            ans = page(base+"/"+sem+"/"+branch+"/"+code+".pdf", check=True)
            if not ans:
              prefix[branch].append(code[:3])
savePaperJson()