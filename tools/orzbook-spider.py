#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os
import re
import sys
import logging
import requests

books_dir = "/data1/download/orzbook/"
done_path = "/data1/download/orzbook-done.txt"
book_path = "/data1/download/orzbook-books.txt"

site = 'http://orzbook.com'
referer = 'http://orzbook.com/22360.html'
NOT_FOUND = u'服务器人数在线过多，请稍等一下再刷新'

headers = {
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer': referer,
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
}


re_list = r'''http://orzbook.com/date/\d+/\d+'''
re_book = r'''http://orzbook.com/(\d+)\.html'''

done_urls = set( line.strip() for line in open(done_path).readlines() )

s = requests.Session()
def get(path):
    if not path.startswith("http"):
        if not path.startswith("/"):
            path = "/" + path
        path = site + path
    return s.get(path, headers=headers, timeout=60)

def download(name, url):
    if url in done_urls:
        logging.info(" skip %-30s %s" % (url, name))
        return
    else:
        logging.info("Visit %-30s %s" % (url, name))
        done_urls.add(url)

    rsp = get(url)
    title = re.findall(u'''文件名称：.*《(.*)》''', rsp.text)
    if not title: return
    title = title[0]
    passwd = re.findall(u'''提取码:([^\)]*)''', rsp.text)
    if not passwd: return
    passwd = passwd[0]
    link = re.findall(r'https?://pan.baidu.com/s/[^ ]*', rsp.text)[0]
    t = u"%s\t%s\t%s\t%s\n" % (name, link, passwd, title)
    open(book_path, "a").write( t.encode("UTF-8") )
    print t


def visit_list(page):
    idx = 0
    while True:
        idx += 1
        rsp = get( page + "/page/%d" % idx )
        if NOT_FOUND in rsp.text: break
        for book in set(re.findall(re_book, rsp.text)):
            download( book, "http://orzbook.com/download.php?id=%s" % book)

def visit_index():
    rsp = get("/")
    for url in re.findall(re_list, rsp.text):
        visit_list(url)
        open(done_path, "w").write("\n".join(done_urls))

def main():
    visit_index()

if __name__ == "__main__":
    logging.basicConfig(
            format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level = logging.DEBUG
            )
    sys.exit(main())

