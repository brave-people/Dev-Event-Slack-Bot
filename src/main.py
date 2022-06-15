
# slack core
from core.core import SlackAPI

slack = SlackAPI(conf="test")
slack.post_text_message("C034R2SQRDY", "테스트")