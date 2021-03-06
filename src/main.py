
# custom lib
import os
from core.slack import SlackAPI
from core.config import set_env
from crawler.crawler import crawler_run

# 환경변수 세팅
set_env(["slack_token", "event_check_url"])

# monitor
# dict( url: str(변화감지된 url), msg: str(html) )
msg_txt_list: list[dict] = crawler_run()

# 변동 감지된 링크가 있다면
if len(msg_txt_list) > 0:
    # slack 
    slack = SlackAPI(debug=True)
    target_channels = slack.get_channel_info()

    # msg_txt_list - hook all
    for msg_txt in msg_txt_list:
        for target_ch in target_channels:
            # 채널에 추가하고, 멤버로 초대를 해야만 message를 보낼 수 있다
            if target_ch['is_member']: 
                slack.post_text_message(target_ch['id'], f"{msg_txt} to {target_ch['name']}")



# 훅 보낸 뒤에 보낸 로그 파일을 csv 파일로 만들어 두자 
