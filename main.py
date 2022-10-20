
# python lib
import os
from time import perf_counter_ns, process_time_ns

# custom lib
from core import exception_handler
from core.slack import SlackAPI
from core.config import set_env
from core.db.mongodb import Repository
from crawler.crawler import crawler_run


def send_slack_msgs(msg_txt_list: list[dict], repository: Repository):
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
                repository.log_data(
                    "hook_log",
                    f"{target_ch['id']}, {target_ch['name']}, {msg_dict.get('url')}"
                )
                slack.post_text_message(
                    target_ch['id'], msg_dict.get("img"), msg_dict.get("msg")
                )


if __name__ == "__main__":
    start_time = perf_counter_ns()  # 1ns * 10^9 = 1s
    process_start_time = process_time_ns()

    # 환경변수 세팅 - 배포 환경, 헤로쿠에서는 set_env 필요 X
    # set_env(["slack_token", "event_check_url", "mongodb_atlas_url"])

    # DBMS object
    repository = Repository()
    repository.log_data("process_start")

    # monitor
    try:
        # dict( url: str(변화감지된 url), img: str(url), msg: list[list] )
        msg_txt_list: list[dict] = crawler_run(repository)

        # 변동 감지된 링크가 있다면
        if len(msg_txt_list) > 0:
            send_slack_msgs(msg_txt_list, repository)

        end_time = perf_counter_ns()
        process_end_time = process_time_ns()
    except Exception as exc:
        exception_handler(exc, repository)

    # logging
    repository.log_data(
        "run_log",
        f"total run time: {end_time - start_time} ms {(end_time - start_time) * 0.000000001} second"
    )
    repository.log_data(
        "run_log",
        f"process run time: {process_end_time - process_start_time} ms {(process_end_time - process_start_time) * 0.000000001} second"
    )
