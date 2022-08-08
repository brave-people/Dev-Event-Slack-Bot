
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

    def __init__(self) -> None:
        self.STANDARD_GIT_URL = "https://github.com"
        self.FILE_PATH = f'{os.environ.get("base_dir")}/data/standard_url.csv'


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
            read_url_list = list() # "\n" 이스케이프를 위해 file.readlines 바로 저장X
            with open(self.FILE_PATH, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    read_url_list.append(line.replace("\n",""))
            return read_url_list
        # 존재하지 않으면
        else:  
            return self.set_standard_data(self.data_parsing())


    def set_standard_data(self, issue_url_list: list[str]) -> list[str]:
        """
        변화의 기준이 되는 standard 데이터 쓰기, signle 컬럼
        """
        with open(self.FILE_PATH, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            for url in issue_url_list:
                writer.writerow([url])

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
            try:
                href = issue.find('a').get('href')
                if "q" in str(href): continue # 쓸모 없는 issue
                else: issue_url_list.append(issue.find('a').get('href'))
            except AttributeError:
                continue # 쓸모없는 div 경우

        return_issue_url_list = list(set(issue_url_list)) # 중복 제거
        return_issue_url_list.sort(reverse=True)
        return return_issue_url_list 


    def data_detail_parsing(self, target_url):
        """
        변화감지로 잡힌 issue의 url에서 detail한 정보를 parsing해 옴, hook 보낼 정보들임
        """
        html = self.get_html(target_url=target_url)
        main_table = html.find('table')
        txt_image = main_table.select_one("tbody > tr:nth-child(1) > td > div > a").find('img').get('src')
        txt_tag = main_table.select_one("tbody > tr:nth-child(1) > td > p:nth-child(3)")
        a_tag_list = txt_tag.find_all('a')
        
        # text 재조합하기
        return_txt_list = list()
        temp = ""
        for i, txt in enumerate(txt_tag.get_text().strip().split("\n")):
            # text 덩어리 3개씩 조합됨, 0일때 tag가 달림
            if i % 3 == 0:
                return_txt_list.append(temp)
                temp = list()
                temp.append(txt)
                temp.append(a_tag_list[int(i / 3)].get('href'))
            else:
                temp.append(txt)
        return txt_image, return_txt_list[1:]


    def data_compare(self) -> list[dict]:
        """
        standard 데이터와 지금 긁어온 데이터 리스트 비교, 달라지면 변화 감지
        그리고 standard를 update 한다. 
        return - 감지된 변화에 대해 훅 보낼 데이터 
        """
        # return 할 list[dict]
        return_hook_data = list()

        # step1. standard data 가져오기
        standard_data_list = self.get_standard_data()

        # step2. target url에서 issue의 url list 가져오기
        new_issue_url_list = self.data_parsing()

        # step3. 두 list에서 다른 값 가져오기 (다른 url 가져오기), 여러개일 수 있어서 list로 계속 취급
        result_diff_list = list(set(new_issue_url_list) - set(standard_data_list))

        # step4. 다른 url을 타고 들어가서 상세 정보를 한 번 더 파싱해오기
        if len(result_diff_list) > 0:
            # hook 보낼 정보 생성
            for result in result_diff_list:
                target_url = f"{self.STANDARD_GIT_URL}{result}"
                hook_image, hook_msg = self.data_detail_parsing(target_url)
                return_hook_data.append(dict(
                    url=target_url,
                    img=hook_image,
                    msg=hook_msg
                ))

            # 해당 url 로 update
            self.set_standard_data(new_issue_url_list)

        # 해당 상세 정보를 return 하기
        return return_hook_data


def crawler_run():
    """
    크롤링 원하는 목적, 결과 데이터만 리턴하기 (Crawler class참조)
    해당 결과 데이터는 slack bot을 통해 msg로 나갈 list들
    """
    crawl = Crawler()
    return crawl.data_compare()