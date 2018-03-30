#coding:utf-8
import re,json
from bs4 import BeautifulSoup
from urllib import parse,request
if __name__ == "__main__":
    ip = "http://v.youku.com/v_show/id_XMzQ3OTk5Nzk0OA==.html?spm=a2hww.20027244.m_250239.5~5~5~5!2~5~5~A"
    get_url = "http://www.a305.org/tong.php?url=%s"%ip
    get_movie_url = 'http://www.a305.org/x1/api.php'
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Referer": "http://www.a305.org/tong.php?url=%s" % ip,
    }
    get_url_req = request.Request(url= get_url,headers=head)
    get_url_response = request.urlopen(get_url_req)
    get_url_html = get_url_response.read().decode("utf-8")
    bf = BeautifulSoup(get_url_html,'lxml')
    print(bf.body)





