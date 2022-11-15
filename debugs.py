
# python lib
import os
from time import perf_counter_ns, process_time_ns

# custom lib
from core.slack import SlackAPI
from core.config import set_env

if __name__ == "__main__":
    # 환경변수 세팅 - 배포 환경, 헤로쿠에서는 set_env 필요 X
    set_env(["slack_token", "event_check_url", "mongodb_atlas_url"])

    slack = SlackAPI(debug=True)
    target_channels = slack.get_channel_info()

    # print(target_channels)