# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pymongo import MongoClient


# AWS EC2 서버에 있는 mongodb와 연결

# 본인 AWS EC2 주소
server = 'ec2-35-164-25-57.us-west-2.compute.amazonaws.com'

# MongoClient 객체 생성
mongo = MongoClient(server, 27017)

# mongodb(db 이름: playwings, collection 이름: flypeach)
flypeach = mongo.playwings.flypeach


# mongodb 쿼리 구성 파일
class EventDAOF(object):

    def __init__(self):
        pass

    # mongodb에 저장 쿼리
    def save_events(self, link, title):

        # saved Flag False로 초기화
        saved = False

        # 기존 flypeach collection에 존재하면 저장하지않고 없으면 저장하고 saved Flag True로 변경
        if not self.get_events_by_id(link):
            flypeach.insert_one({'link': link, 'title': title})
            saved = True
            # news.update_one({'link': link}, {'$set': {'title': title, 'content': content, 'written_time': written_time, 'crawl_time': crawl_time}}, upsert=True)
        return saved

    # db내 중복 점검 쿼리문 작성
    def get_events_by_id(self, link):

        # 고유 primary_key인 link로 search 쿼리
        result = flypeach.find({'link': link})

        # search 결과 존재하면 True반환, 없을 경우 False반환
        if result.count() > 0:
            return True

        return False
