# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import datetime
import requests
from bs4 import BeautifulSoup
from mongodb_jinair import EventDAO


class JinAirCrawler(object):

    # 크롤러 초기화(mongodb 쿼리작성파일 연결)
    def __init__(self, eventdao):
        self.eventdao = eventdao

    # 마지막 페이지 변수를 받아 루프 돌며 크롤링 진행
    def get_pages_content(self, last_page_number):
        list1 = []
        list2 = []

        for i in xrange(1, last_page_number + 1):

            # 페이지 번호에 따른 url
            url = 'http://www.jinair.com/HOM/Event/Event01List.aspx?page={}&keyfield=1&keyword=&mid='.format(i)

            # 각 게시물 url 생성을 위한 기본 문자열
            content_url = 'http://www.jinair.com/HOM/Event/Event01View.aspx?page={}&seq={}&num={}&keyfield={}&keyword=&mid='

            # 페이지 번호 순으로 크롤링 시작
            try:
                res = requests.get(url)
                content = res.content
                soup_1 = BeautifulSoup(content, 'html.parser')

                # 제목 및 게시글 link 생성을 위한 인자 추출
                for k in soup_1.find_all('nobr'):

                    # 제목 추출
                    title = k.get_text()

                    # page number, seq번호, 게시글 순서번호, keyfield 번호
                    page = k.a['onclick'].split('"')[1]
                    seq = k.a['onclick'].split('"')[3]
                    num = k.a['onclick'].split('"')[5]
                    keyfield = k.a['onclick'].split('"')[7]

                    # 게시글 link완성
                    link = content_url.format(page, seq, num, keyfield)

                    # 게시글 링크, 제목 튜플화 시켜 list로 저장
                    list1.append(tuple((link, title)))


                # 이벤트 기간 크롤링을 위한 BeautifulSoup 사용
                for j in soup_1.find_all('span', id=lambda x: x and x.endswith('lblEventTerm')):

                    # 이벤트 시작 - 종료기간
                    event_date = j.get_text().split(' ~ ')

                    # 이벤트 기간 tuple화 후 list에 저장
                    list2.append(tuple(event_date))

            # 예외처리 및 오류 출력
            except Exception as e:
                print '1', e

        # 링크, 제목 list와 이벤트 기간 list의 인자를 받아 DB 저장 parameter로 한꺼번에 전달
        for x, y in zip(list1, list2):

            link = x[0]
            title = x[1]
            start_date = y[0]
            end_date = y[1]

            try:
                # DB로 연결: 각 게시글이 DB에 존재하면 저장하지않고, 존재하지 않으면 저장함.
                if self.eventdao.save_events(link, title, start_date, end_date):
                    # 새로운 이벤트면 저장하고 알람 메서드 호출
                    self.get_alarm(link, title, start_date, end_date)

                # 새로운 이벤트 없으면 없다고 출력
                else:
                    self.no_new_events()

            # 예외처리 및 오류메시지 출력
            except Exception as e:
                print '2', e


    # 게시판 마지막 페이지 번호 추출 메서드
    def get_last_page_number(self, url):

        res = requests.get(url)
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')

        # 게시판 페이지 번호를 추출하여 크롤링 진행
        for j in soup.find_all('ul', attrs={"class": "paging"}):

            # 페이지 번호 추출
            try:
                # 마지막 page정보가 있다면 추출하여 전달
                if j.a.get_text():
                    last_page_number = int(j.a.get_text())
                    self.get_pages_content(last_page_number)

            # 에러메시지 출력
            except Exception as e:
                print '1', e

            # 마지막 페이지가 1페이지라면 페이지 전달하여 1페이지 크롤링
            finally:
                last_page_number = int(j.strong.get_text())
                self.get_pages_content(last_page_number)

    # 새로운 이벤트가 생성됐을시 알람
    def get_alarm(self, link, title, start_date, end_date):
        print '------------------------------------------'
        print 'JinAirCrawler'
        print title
        print 'link : {}'.format(link)
        print '이벤트 기간 : {} ~ {}'.format(start_date, end_date)
        print '------------------------------------------'

    # 새로운 이벤트 없을시의 알람
    def no_new_events(self):
        print '--------------------'
        print 'NO NEW EVENTS TT'
        print 'NO NEW EVENTS TT'
        print 'NO NEW EVENTS TT'
        print '--------------------'


# 5분마다 batch로 실행반복 메서드
# def Repeat():
#
#     # 크롤링 시작 화면 출력
#     print '*' * 80
#     print time.ctime(), 'CRAWL START!!!!!'
#     print '*' * 80

#     # 크롤링 시작 url
#     origin_url = 'http://www.jinair.com/HOM/Event/Event01List.aspx'
#
#     # 크롤링 시작 메서드 호출
#     eventdao = EventDAO()
#     crawler = JinAirCrawler(eventdao)
#     crawler.get_last_page_number(origin_url)
#
#     # Repeat()메서드 300초 후에 다시 시작
#     threading.Timer(60, Repeat).start()
#
# Repeat()


# 크롤링 시작시 필요한 변수 선언 및 객체생성
if __name__ == '__main__':

    # 크롤링 시작 url
    origin_url = 'http://www.jinair.com/HOM/Event/Event01List.aspx'
    eventdao = EventDAO()
    crawler = JinAirCrawler(eventdao)
    crawler.get_last_page_number(origin_url)
