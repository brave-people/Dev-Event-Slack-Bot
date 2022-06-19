
# python lib
import os, json
from pathlib import Path
from typing import List
 

def get_secret_file(base_dir: str):
    """
    secret file import - 환경변수값 세팅을 위해  
    """
    config_json = None
    try:
        with open(os.path.join(base_dir, 'secrets.json'), 'rb') as secret_file:
            config_json = json.load(secret_file)
    except Exception as e:
        raise Exception(f"setting config error: {e}, {type(e).__name__}, {type(e)} [AT {base_dir}.settings]")

    if config_json is None:
        raise Exception(f"setting config error: 세팅 값이 NONE이 될 수 없습니다. [AT {base_dir}.settings]")

    return config_json



def set_env(key_list: List[str]) -> None:
    """
    secret file 기반으로 OS 환경 변수 설정
    """
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    config = get_secret_file(BASE_DIR)
    for key in key_list: os.environ[key] = config[key]

    # ps - 해당 프로젝트 최상위 경로, base directory 기억
    os.environ["base_dir"] = BASE_DIR
