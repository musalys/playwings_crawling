항공권 특가 크롤러
====================
진에어 및 피치항공 특가 정보 크롤링을 위해 제작되었습니다.
코딩은 파이썬을 사용하였고, DB는 MongoDB를 사용하였습니다.

크롤러 구동 방법
------------
* crontab.py 파일을 실행시킵니다. (60초마다 재실행하도록 설정되었습니다.) 바꾸려면 파일안의 초를 바꾸면 됩니다.

# 파일 구성
* jinair_crawler.py : 진에어 이벤트 게시판의 특가 정보를 스크래핑합니다. 홈페이지는 [여기][url]에서 확인할 수 있습니다.
[url]: http://www.jinair.com/HOM/Event/Event01List.aspx 

* flypeach_crawler.py : 피치항공의 특가 정보를 스크래핑합니다. 홈페이지는 [여기][urlf]에서 확인할 수 있습니다.
[urlf]: http://www.flypeach.com/pc/kr

* mongodb_jinair.py
    * 스크래핑한 진에어 특가정보를 서버의 MongoDB에 저장합니다. 연결을 위해 자신의 서버 호스트와, 포트 넘버가 필요합니다.

* mongodb_flypeach.py
    * 스크래핑한 피치항공 특가정보를 MongoDB에 저장합니다. 연결을 위해 자신의 서버 호스트와, 포트 넘버가 필요합니다.

* crontab.py
    * 위의 전체 파일들을 원하는 주기마다 실행시키는 파일입니다.
    
# 구동환경
* python 2.7.12
* MongoDB
* AWS EC2
* Packages : BeautifulSoup, requests, pymongo, time, threading
