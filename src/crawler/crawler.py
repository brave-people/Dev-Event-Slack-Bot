
# python lib
import os, csv
from requests import get
from bs4 import BeautifulSoup
from typing import Any, List

# custom lib
from core.exception_handler import exception_handler

class Crawler:
    """
    범용성 X, 특수 목적, 특수 url 크롤링 및 타겟 변화감지 모니터링
    """
    STANDARD_GIT_URL = "https://github.com"
    FILE_PATH = f'{os.environ.get("base_dir")}/data/csv/standard_url.csv'

    def __init__(self) -> None:
        pass


    def get_html(self, target_url=None):
        """
        특정 url을 통해 특정 data 들고오기, header 값 필요 X
        """
        try:
            url = os.environ.get("event_check_url") if isinstance(target_url, type(None)) else target_url
            res = get(url, timeout=3)
            return BeautifulSoup(res.content, 'lxml')
        except Exception as exc:
            return exception_handler(exc)


    def get_standard_data(self) -> list[str]:
        """
        변화의 기준이 되는 standard 데이터 가져오기, 없으면 만들기
        """

        # 존재하면
        if os.path.isfile(self.FILE_PATH):
            with open(self.FILE_PATH, 'r', encoding='utf-8') as file:
                return file.readlines()
        # 존재하지 않으면
        else:  
            return self.set_standard_data(self.data_parsing())


    def set_standard_data(self, issue_url_list: list[str]) -> list[str]:
        """
        변화의 기준이 되는 standard 데이터 쓰기
        """
        with open(self.FILE_PATH, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(issue_url_list)

        return issue_url_list


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


    def data_detail_parsing(self, target_url):
        """
        변화감지로 잡힌 issue의 url에서 detail한 정보를 parsing해 옴, hook 보낼 정보들임
        """
        html = self.get_html(target_url=target_url)


    def data_compare(self):
        """
        standard 데이터와 지금 긁어온 데이터 리스트 비교, 달라지면 변화 감지
        그리고 standard를 update 한다. 
        return - 감지된 변화에 대해 훅 보낼 데이터 
        """

        # step1. standard data 가져오기
        standard_data_list = self.get_standard_data()

        # step2. target url에서 issue의 url list 가져오기
        new_issue_url_list = self.data_parsing()

        # step3. 두 list에서 다른 값 가져오기 (다른 url 가져오기)


        # step4. 다른 url을 타고 들어가서 상세 정보를 한 번 더 파싱해오기

        # 해당 상세 정보를 return 하기



def crawler_run():
    crawl = Crawler()
    return crawl.data_compare()