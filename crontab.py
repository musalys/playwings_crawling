# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time, threading
import datetime

from jinair_crawler import JinAirCrawler
from flypeach_crawler import FlyPeachCrawler
from mongodb_jinair import EventDAOJ
from mongodb_flypeach import EventDAOF


# 5분마다 batch로 실행반복 메서드
def batch_repeat():

    # 크롤링 시작 화면 출력
    print '*' * 80
    print 'CRAWL START!!!!!', time.ctime()
    print '*' * 80

    # 크롤링 시작 url
    origin_url_j = 'http://www.jinair.com/HOM/Event/Event01List.aspx'
    origin_url_f = 'http://www.flypeach.com/pc/kr'

    # db파일 연결
    eventdaoj = EventDAOJ()
    eventdaof = EventDAOF()

    # 크롤링 객체 생성 및 실행
    jinair_crawl = JinAirCrawler(eventdaoj)
    jinair_crawl.get_last_page_number(origin_url_j)

    flypeach_crawl = FlyPeachCrawler(origin_url_f, eventdaof)
    flypeach_crawl.get_sales_promos()

    # Repeat()메서드 60초 후에 다시 시작
    threading.Timer(60, batch_repeat).start()

batch_repeat()
