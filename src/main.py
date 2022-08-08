
# python lib
import os
from time import perf_counter_ns, process_time_ns

# custom lib
from logger import log, process_start_log
from core.slack import SlackAPI
from core.config import set_env
from core.exception_handler import exception_handler
from crawler.crawler import crawler_run


def send_slack_msgs(msg_txt_list: list[dict]):
    '''
    bot을 추가한 모든 채널에 message 보내는 최상위 함수
    - standard_url.csv에 변동된 url이 감지되어야만 러닝
    - msg_txt_list의 데이터 형태가 중요함
    '''

    # slack 
    slack = SlackAPI(debug=True)
    target_channels = slack.get_channel_info()

    # msg_dict - # dict( url: str(변화감지된 url), img: str(url), msg: list[list] )
    for msg_dict in msg_txt_list:

        # 채널에 추가하고, 멤버로 초대를 해야만 message를 보낼 수 있다
        for target_ch in target_channels:
            if target_ch['is_member']: 
                log(f"msg hook tried: {target_ch['id']}, {target_ch['name']}, {msg_dict.get('url')}")
                slack.post_text_message(target_ch['id'], msg_dict.get("img"), msg_dict.get("msg"))



if __name__ == "__main__":
    start_time = perf_counter_ns() # 1ns * 10^9 = 1s
    process_start_time = process_time_ns()
    process_name = "dev-event-slack-bot"
    process_start_log(process_name)

    # 환경변수 세팅
    set_env(["slack_token", "event_check_url"])

    # monitor
    try:
        # dict( url: str(변화감지된 url), img: str(url), msg: list[list] )
        msg_txt_list: list[dict] = crawler_run()

        # 변동 감지된 링크가 있다면
        if len(msg_txt_list) > 0:
            send_slack_msgs(msg_txt_list)

        end_time = perf_counter_ns()
        process_end_time = process_time_ns()
    except Exception as exc:
        exception_handler(exc)
        
    log(f"{process_name} total run time: {end_time - start_time} ms {(end_time - start_time) * 0.000000001} second")
    log(f"{process_name} process run time: {end_time - start_time} ms {(end_time - start_time) * 0.000000001} second")