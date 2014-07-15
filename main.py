#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'bong'

import urllib2
import json
import re
from lxml import etree
from dateutil import parser as dparser

"""
page num is review page num
@:param m is total page num
"""
def ktreviews(id):
    pid = id
    i = 1
    url = "http://market.olleh.com//appDetail?ptype=C&category=&pid="+ pid +"&page="+ str(i) +"&tab=3&sel_order=1"
    resp = urllib2.urlopen(url)
    dom = resp.read()
    parser = etree.HTMLParser()
    result = etree.fromstring(dom, parser=parser)
    review = result.findall(".//div[@class='tab_use']//li")

    page = result.findall(".//div[@class='tab_use']//div[@class='cocmBrdPaging']//span[@class='whole']")
    print len(review)
    tn = int(re.findall('[0-9]+',page[0].text)[0])
    if tn is not 0 :
        print "page number is %d"% tn
        for pn in range(tn, 0, -1) :
            url = "http://market.olleh.com//appDetail?ptype=C&category=&pid=51200015902624&page="+ str(pn) +"&tab=3&sel_order=1"
            resp = urllib2.urlopen(url)
            dom = resp.read()
            parser = etree.HTMLParser()
            result = etree.fromstring(dom, parser=parser)
            reviews = result.findall(".//div[@class='tab_use']//li")
            length = len(reviews)
            print "No.%d review result count is %d" % (pn, len(reviews))

            for rvn in xrange(0, length, 2):
                #print reviews[rvn]
                name = reviews[rvn].find(".//div[@class='name']").text.encode("utf-8").strip()
                star = reviews[rvn].find(".//div[@class='name']/img").attrib['title'].encode("utf-8")
                date = dparser.parse(re.sub("[\(|\)]+","",reviews[rvn].find('.//div[@class="date"]').text.encode("utf-8").strip()))
                #favor = reviews[rvn].find(".//a")
                #print etree.tostring(favor,encoding="UTF-8",method="html");
                contents = reviews[rvn +1].find(".//span").text.encode("utf-8").strip()

                print "name : %s, star: %s, date: %s, favor: %s, contents : %s" % (name, star, date, None, contents)


    else:
        print "%d is 0" % tn


    #print result

def skreviews():
    r = ()
    i = 300
    while True:
        url = "http://www.tstore.co.kr/userpoc/common/reply/ajaxReplyInfo?prodId=0000643921&offset=" + str(i)
        print url
        try:
            resp = urllib2.urlopen(url)
            data = json.loads(resp.read())
            if data["notiList"] is None:
                break
            i += 1
        except:
            break
    print i


def main():
   # skreview()
    ktreviews("51200015902624")

if __name__ == "__main__":
    print "author is {0}".format(__author__)
    main();
