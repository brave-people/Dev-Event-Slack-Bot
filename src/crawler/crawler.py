
# python lib
import os
from requests import get
from bs4 import BeautifulSoup
from typing import List

# custom lib
from core.exception_handler import exception_handler

class Crawler:
    """
    범용성 X, 특수 목적, 특수 url 크롤링 및 타겟 변화감지 모니터링
    """
    STANDARD_GIT_URL = "https://github.com"


    def __init__(self) -> None:
        pass



    def get_html(self):
        """
        특정 url을 통해 특정 data 들고오기, header 값 필요 X
        """
        try:
            url = os.environ.get("event_check_url")
            res = get(url, timeout=3)
            return BeautifulSoup(res.content, 'lxml')
        except Exception as exc:
            return exception_handler(exc)


    def get_standard_data(self):
        """
        변화의 기준이 되는 standard 데이터 가져오기, 없으면 만들기
        """
        pass


    def data_parsing(self) -> List[str]:
        """
        DOM 중 타겟 DOM의 데이터만 가져오기, 여기서는 issue의 url만 가져올 것
        """
        
        html = self.get_html()
        main_div = html.find("div", {"id": "repo-content-pjax-container"})
        issue_lists = main_div.find("div", {"class": "js-navigation-container js-active-navigation-container"}).find_all('div')

        # issue url list 
        issue_url_list = list()
        for issue in issue_lists:
            issue_url_list.append(issue.find('a').get('href'))

        return issue_url_list


    def data_compare(self):
        """
        standard 데이터와 지금 긁어온 데이터 리스트 비교, 달라지면 변화 감지
        그리고 standard를 update 한다. 
        return - 감지된 변화에 대해 훅 보낼 데이터 
        """