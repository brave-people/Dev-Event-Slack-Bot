
# slack core
from core.slack import SlackAPI
from core.config import set_env

# 환경변수 세팅
set_env(["slack_token", "event_check_url"])

# slack 
slack = SlackAPI(debug=True)
target_channels = slack.get_channel_info()
for target_ch in target_channels:
    # 채널에 추가하고, 멤버로 초대를 해야만 message를 보낼 수 있다
    if target_ch['is_member']:
        slack.post_text_message(target_ch['id'], f"테스트 to {target_ch['name']}")
