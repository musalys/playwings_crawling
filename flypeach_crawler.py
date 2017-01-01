# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
from mongodb_flypeach import EventDAO

class FlyPeachCrawler(object):

    def __init__(self, origin_url, eventdao):
        self.origin_url = origin_url
        self.eventdao = eventdao

    # 특전/캠페인 탭에서 진행사항이 존재할 경우 크롤링 메서드
    def get_sales_promos(self):

        # request및 BeautifulSoup 사용으로 코드 추출
        res = requests.get(self.origin_url)
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')

        # flypeach항공 메인페이지에서 특전/캠페인 탭에 진행하는 세일/프로모션 있는지 확인 후 있으면 링크 전달
        for j in soup.find_all('li', attrs={'class': ['nicon campaign cf', 'nicon sale cf']}):

            # ul, li, a, href 값이 없을 경우 대비하여 예외처리
            try:
                # 프로모션 및 특가 정보가 있다면 링크 추출 및 get_content 메서드 호출
                if j.ul.li.a['href']:
                    # print j.ul.li.a.get_text().strip()
                    # print j.ul.li.a['href']
                    link = j.ul.li.a['href']

                    # print 'method 1'
                    self.get_content(link)

            # 에러메시지 출력
            except Exception as e:
                print '1', e
                self.get_link_from_main_page()

            # 이 방법이 실패했을 경우, 최종 실행 내용 및 메인 페이지 링크 추출 메서드 호출
            # finally:
            #    print 'end1'
            #    self.get_link_from_main_page()

    # 메인페이지의 전체 링크와 캠페인 및 세일 url을 비교하여 세일 및 프로모션 링크 추출
    def get_link_from_main_page(self):

        # 세일/캠페인이 진행중인 것들의 기본 link
        campaign = 'http://www.flypeach.com/pc/kr/um/specials/campaign/'
        sale = 'http://www.flypeach.com/pc/kr/um/specails/sale/'

        # request및 BeautifulSoup 사용으로 코드 추출
        res = requests.get(self.origin_url)
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')

        # None값 대비 예외처리
        try:

            # 링크 추출
            for k in soup.find_all('a', href=True):

                # campaign 및 sale url 포함되면 url로 간주하고 저장
                if (campaign or sale) in k['href']:

                    # print k['href']
                    link = k['href']

                    # print 'method 2'
                    self.get_content(link)

                # print 'NO PROMOTIONS!!'

        # 에러 출력
        except Exception as e:
            print '2', e

        # 최종 출력
        # finally:
        #     print 'end2'


    # 프로모션의 내용을 크롤링 하는 method
    def get_content(self, url):

        res = requests.get(url)
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')

        # 프로모션 내용 크롤링
        try:
            # 제목 및 링크 추출
            for k in soup.find_all('div', attrs={'class': 'breadcrumb'}):

                # 제목 출력 test
                # print k.find(href=url).get_text()
                title = k.find(href=url).get_text()

                # 프로모션 결과 저장(존재하면 저장, 존재하지 않으면 저장X)
                if self.eventdao.save_events(url, title):
                    print 'NEW PROMOTIONS!!'

                print 'NO PROMOTIONS.'


        # 예외처리
        except Exception as e:
            print '3', e

        # 최종 출력
        # finally:
        #     print 'end3'

# 크롤링 page
origin_url = 'http://www.flypeach.com/pc/kr'

eventdao = EventDAO()
crawler = FlyPeachCrawler(origin_url, eventdao)
crawler.get_sales_promos()
