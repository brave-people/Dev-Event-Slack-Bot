
# python lib
import ssl, certifi  # CERTIFICATE_VERIFY_FAILED error
from pathlib import Path
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# typing
from slack_sdk.web.slack_response import SlackResponse

# extentions
from .config import get_secret_file

class SlackAPI:
    """
    슬랙 API 핸들러
    """
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def __init__(self, **kwargs):
        config = get_secret_file(self.BASE_DIR)  # slack API를 위한 환경 변수 값 세팅
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(config['slack_token'], ssl=ssl_context)  # 슬랙 클라이언트 인스턴스 생성
        self.__dict__.update(kwargs)  # 변동 가능성 있는 변수값 위해 kwargs 세팅


    def get_channel_info(self) -> list:
        """
        슬랙에 해당 봇을 추가한 워크스페이스의 모든 채널 info 가져오기 
        """
        # conversations_list() 메서드 호출
        result = self.client.conversations_list() # slack bot에 대한 정보 나열
        
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels'] # 그 중 slack bot이 추가된 channel에 대한 리스트업
        return channels


    def post_text_message(self, channel_id: str, msg: str) -> SlackResponse:
        """
        슬랙 봇 추가한 channel_id 로 해당 msg 전송하기
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=msg
            )
            return response
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'


    # ================================================================= #
    # 이하 Optional 한 method 들 
    # ================================================================= #


    def get_channel_id_by_name(self, channel_name):
        """
        슬랙 채널명으로 채널ID 조회
        """
        # conversations_list() 메서드 호출
        result = self.client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels']
        # 채널 명이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id


    def get_message_ts(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        # conversations_history() 메서드 호출
        result = self.client.conversations_history(channel=channel_id)
        # 채널 내 메세지 정보 딕셔너리 리스트
        messages = result.data['messages']
        # 채널 내 메세지가 query와 일치하는 메세지 딕셔너리 쿼리
        message = list(filter(lambda m: m["text"]==query, messages))[0]
        # 해당 메세지ts 파싱
        message_ts = message["ts"]
        return message_ts


    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text = text,
            thread_ts = message_ts
        )
        return result
