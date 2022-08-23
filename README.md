# Dev-Event-Slack-Bot
> 🎉🎈 개발자 행사를 슬랙 봇으로 알려드립니다.


## Getting Start 

- 해당 slack bot을 워크스페이스에 추가한다.
- 추가된 앱을 눌러서 채널에 추가를 해야한다. (채널에 해당 bot 초대)
- 기본적으로 필요한 권한은 아래와 같다.
    - calls:write = Start and manage calls in a workspace
    - channels:read = View basic information about public channels in a workspace
    - chat:write = Send messages as @dev-event
    - groups:read = View basic information about private channels that 개발자-행사-구독-Test has been added to
    - im:read = View basic information about direct messages that 개발자-행사-구독-Test has been added to
    - mpim:read = View basic information about group direct messages that 개발자-행사-구독-Test has been added to


## How To Add Slack Bot

- B

---

## How To Work

1. Dev-Event-Subscribe 의 “issues” 를 크롤링 합니다.
2. 크롤링 한 정보를 csv 파일로 저장합니다.
3. 최초시 csv 를 만듭니다 (csv가 존재하지 않으면 최초로 인식)
    - 최초가 아닐 경우, 이미 있는 csv 파일 (과거의 것) 과 새롭게 크롤링한 정보와 대조합니다.
    - 정확하게는 issue의 url 를 체크합니다.
4. 바뀐 것이 있으면 변화(새롭게 올라온 것으로)로 여기고, 훅을 보낼 데이터를 만들고, 이벤트 정보를 모두 훅 합니다
5. 그리고 바뀐 것으로 csv를 다시 저장합니다.


https://app.slack.com/block-kit-builder