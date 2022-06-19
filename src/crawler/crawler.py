

class Crawler:
    """
    범용성 X, 특수 목적, 특수 url 크롤링 및 타겟 변화감지 모니터링
    """


    def __init__(self) -> None:
        pass



    def get_html(self):
        """
        특정 url을 통해 특정 data 들고오기, header 값 필요 X
        """
        pass


    def get_standard_data(self):
        """
        변화의 기준이 되는 standard 데이터 가져오기, 없으면 만들기
        """
        pass


    def data_compare(self):
        """
        standard 데이터와 지금 긁어온 데이터 리스트 비교, 달라지면 변화 감지
        그리고 standard를 update 한다. 
        return - 감지된 변화에 대해 훅 보낼 데이터 
        """