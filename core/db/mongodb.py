
# python lib
import os
import pymongo
import certifi
from datetime import datetime
from pytz import timezone
from typing import Optional

# custom lib
from core import exception_handler


class Repository():
    '''
    mongodb altas connection 과 CRUD transacion - 싱글톤 패턴
    '''

    def __init__(self) -> None:
        # client = pymongo.MongoClient(os.environ.get("mongodb_atlas_url"))
        client = pymongo.MongoClient(
            os.environ.get("mongodb_atlas_url"),
            tlsCAFile=certifi.where()
        )
        self.db = client["dev-event-slack-bot"]
        self.main_coll = self.db["standard-data"]
        self.log_coll = self.db["log-data"]
        self.hook_log_coll = self.db["hook-log-data"]

    def get_standard_data(self) -> dict:
        '''
        "standard-data" collection의 issue url 저장 data (유일)를 하나 가져온다.
        '''
        return self.main_coll.find_one({"attribute": "standard-data"})

    def insert_standard_data(self, issue_url_list: list[str]) -> dict:
        '''
        "standard-data" collection의 issue url 저장 data - `"attribute": "standard-data"` 를 만든다
        - 최초에 한 해 1회 실행 되는 형태
        - insert 후 find 까지 하여 해당 data return
        '''
        try:
            now = datetime.now(timezone('Asia/Seoul')
                               ).strftime('%Y-%m-%d %H:%M:%S')
            self.main_coll.insert_one({
                "attribute": "standard-data",
                "issue_url_list": issue_url_list,
                "created_at": now,
                "updated_at": now
            })
            return self.get_standard_data()
        except Exception as exc:
            print(f"{exc}, {type(exc).__name__}, {type(exc)}")

    def update_standard_data(self, issue_url_list: list[str]) -> dict:
        '''
        "standard-data" collection의 issue url 저장 data (유일)를 update 한다.
        '''
        try:
            now = datetime.now(timezone('Asia/Seoul')
                               ).strftime('%Y-%m-%d %H:%M:%S')
            self.main_coll.update_one({"attribute": "standard-data"}, {"$set": {
                "issue_url_list": issue_url_list,
                "updated_at": now
            }})
            return self.get_standard_data()
        except Exception as exc:
            print(f"{exc}, {type(exc).__name__}, {type(exc)}")

    def log_data(self, log_type: str, log_msg: Optional[str] = None):
        '''
        "log-data" collection에 다양한 형태의 logging을 insert 한다. 
        '''
        try:
            now = datetime.now(timezone('Asia/Seoul')
                               ).strftime('%Y-%m-%d %H:%M:%S')
            if log_type == "process_start":
                self.log_coll.insert_one({
                    "log_type": log_type,
                    "log_msg": "process run start",
                    "created_at": now,
                })

            elif log_type == "hook_log":
                # 채널 id, 채널 명, 후킹 그룹이 될 url
                log_msg_list = log_msg.split(",")
                self.hook_log_coll.insert_one({
                    "log_type": log_type,
                    "target_ch_id": log_msg_list[0].strip(),
                    "target_ch_name": log_msg_list[1].strip(),
                    "hook_group": log_msg_list[2].strip(),
                    "created_at": now,
                })
            else:
                self.log_coll.insert_one({
                    "log_type": log_type,
                    "log_msg": log_msg,
                    "created_at": now,
                })
        except Exception as exc:
            print(f"{exc}, {type(exc).__name__}, {type(exc)}")
