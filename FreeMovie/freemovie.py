#coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import re,json,time
import requests,urlparse,urllib
from bs4 import BeautifulSoup
from selenium import webdriver



class movie_downloader():
    def __init__(self, url):
        self.server = 'http://www.a305.org/x1/api.php'
        self.api = 'http://www.a305.org/tong.php?url='
        self.url = url.split('#')[0]
        self.target = self.api + self.url
        # self.header = {
        #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Cookie": "BAEID=16CF44215D46D8ACE3F8708AC094902E; UM_distinctid=162713a58bb28-0d6e34dc5-36675459-100200-162713a58bce; CNZZDATA1264591021=631636309-1522314337-%7C1522314337"
        # }
        # self.cookie_dict = {'Cookie':"BAEID=16CF44215D46D8ACE3F8708AC094902E; UM_distinctid=162713a58bb28-0d6e34dc5-36675459-100200-162713a58bce; CNZZDATA1264591021=631636309-1522314337-%7C1522314337"}
        # self.cookies = requests.utils.cookiejar_from_dict(self.cookie_dict,cookiejar=None,overwrite=True)
        # self.s = requests.session()
        # self.s.cookies = self.cookies


    def get_key(self):
        pj = webdriver.PhantomJS()
        pj.get(url=self.target)
        time.sleep(2)
        data = pj.page_source
        # req = self.s.get(url=self.target)
        # req = requests.get(url=self.target)
        # req.encoding = "utf-8"
        bf = BeautifulSoup(data, 'lxml')
        a = str(bf.find_all('iframe'))
        pattern = re.compile(r'src="(.*?)"',re.S)
        new_url = "http://www.a305.org"+pattern.findall(a)[0]
        pj.get(url=new_url)
        time.sleep(1)
        data = pj.page_source
        # ras = self.s.get(url=new_url)
        # ras.encoding = "utf-8"
        bf = BeautifulSoup(data, 'lxml')
        a = str(bf.find_all('video'))
        pattern = re.compile(r'src="(.*?)"', re.S)
        src = pattern.findall(a)[0]
        src = urlparse.unquote(src)
        if "iqiyi" in self.target:
            src = src.replace("amp;", "")
            src = "http://www.a305.org"+ src
        else:
            src = src.replace("amp;","")
        pj.close()
        return src
    def point(self,a,b,c):
        per = 100.0*a*b/c
        if per > 100 :
            per = 1
        sys.stdout.write(" "+"%.2f%% 已经下载的大小：%ld 文件大小：%ld"%(per,a*b,c)+ '\r')
        sys.stdout.flush()

    def movie_download(self,url,filename):
        urllib.urlretrieve(url=url,filename=filename,reporthook=self.point)





if __name__ == "__main__":
    while 1:

        url = raw_input("请输入VIP电影URL链接：")
        movie_name = raw_input(u"请输入电影名称：")
        pattern = re.compile(r'[http|https]+://[^\s]*', re.S)
        if pattern.search(url):
            print("请等待...")
            print ("%s下载中："% movie_name)
            mv = movie_downloader(url)
            movie_url = mv.get_key()
            if ".m3u8" in movie_url:
                mv.movie_download(movie_url, movie_name + '.m3u8')
            else:
                movie_url = movie_url.split("\\")[-1]
                mv.movie_download(movie_url,movie_name+'.mp4')
            print "下载完成"
            break
        else:
            print("请输入正确的网址！")



