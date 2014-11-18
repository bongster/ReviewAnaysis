#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'bong'

import urllib2
import urllib
import json
import re
from lxml import etree
from dateutil import parser as dparser

"""
page num is review page num
@:param m is total page num
"""

class Review:
	def __init__(self, storeName, name, title, desc, date):
		self.storeName = storeName
		self.name = title
		self.desc =desc
		self.date = date

def androidReview(id=""):
	pid = id
	url = "https://play.google.com/store/getreviews"
	data = {}
	data['pageNum'] = "1"
	data['id'] = "com.google.android.apps.maps"
	data['reviewSortOrder'] = "1"
	data['xhr'] = "1"
	data['reviewType'] = "0"
	req = urllib2.Request(url)
	f = urllib2.urlopen(req,urllib.urlencode(data))
	dom = f.read()
 	arr = eval(dom[6:])
	print arr[0][2]

def ktreviews(id):
	pid = id
	i = 1
	r = []
	url = "http://market.olleh.com//appDetail?ptype=C&category=&pid="+ pid +"&page="+ str(i) +"&tab=3&sel_order=1"
	resp = urllib2.urlopen(url)
	dom = resp.read()
	parser = etree.HTMLParser()
	result = etree.fromstring(dom, parser=parser)
	page = result.findall(".//div[@class='tab_use']//div[@class='cocmBrdPaging']//span[@class='whole']")
	print page
	tn = int(re.findall('[0-9]+',page[0].text)[0])
	if tn is not 0 :
		for pn in range(tn, 0, -1) :
			url = "http://market.olleh.com//appDetail?ptype=C&category=&pid=51200015902624&page="+ str(pn) +"&tab=3&sel_order=1"
			resp = urllib2.urlopen(url)
			dom = resp.read()
			parser = etree.HTMLParser()
			result = etree.fromstring(dom, parser=parser)
			reviews = result.findall(".//div[@class='tab_use']//li")
			length = len(reviews)
#			print "No.%d review result count is %d" % (pn, len(reviews))
			for rvn in xrange(0, length, 2):
				#print reviews[rvn]
				name = reviews[rvn].find("./div[@class='name']").text.encode("utf-8").strip()
				star = reviews[rvn].find("./div[@class='name']/img").attrib['title'].encode("utf-8")
				date = dparser.parse(re.sub("[\(|\)]+","",reviews[rvn].find('./div[@class="date"]').text.encode("utf-8").strip()))
                #favor = reviews[rvn].find(".//a")
                #print etree.tostring(favor,encoding="UTF-8",method="html");
				contents = reviews[rvn +1].find("./span").text.encode("utf-8").strip()
				r.append(Review("kt",name,star,contents,date))
				print "name : %s, star: %s, date: %s, favor: %s, contents : %s" % (name, star, date, None, contents)
	else:
		print "%d is 0" % tn
	return r
    #print result

def skreviews(id):
	pid = id
	r = []
	i = 1
	while True:
		url = "http://www.tstore.co.kr/userpoc/common/reply/ajaxReplyInfo?prodId="+pid +"&offset=" + str(i)
#		print url
		try:
			resp = urllib2.urlopen(url)
			dataSet = json.loads(resp.read())
			if dataSet["notiList"] is None:
				break
			for data in dataSet["notiList"]:
				notiSeq = data['notiSeq']
				notiTitle = data['notiTitle']
				notiDscr = data['notiDscr'].rstrip()
				regId = data['regId']
				regDt = dparser.parse(data['regDt'])
				r.append(Review("sk",regId,notiTitle,notiDscr,regDt))
#				print "%s %s %s %s %s" % (notiSeq,regId,notiTitle, notiDscr, regDt)
			i += 1
		except BaseException, e:
			print e
			break
	return r

def main():
	print "ing..."
	lists = []
#	skreviews("0000643921")
#	lists.extend(skreviews("0000643921"))
#	lists.extend(ktreviews("51200015902624"))
	androidReview()
	print "result size is %d" % len(lists)
	print "end..."
#    ktreviews("51200015902624")

if __name__ == "__main__":
    print "author is {0}".format(__author__)
    main();
