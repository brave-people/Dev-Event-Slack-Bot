
# slack core
from core.core import SlackAPI

slack = SlackAPI(conf="test")
target_channels = slack.get_channel_info()
for target_ch in target_channels:
    # 채널에 추가하고, 멤버로 초대를 해야만 message를 보낼 수 있다
    if target_ch['is_member']:
        slack.post_text_message(target_ch['id'], f"테스트 to {target_ch['name']}")
