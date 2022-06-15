
# python lib
import os, json

# secret file import - 환경변수값 세팅을 위해
def get_secret_file(base_dir: str):
    config_json = None

    try:
        with open(os.path.join(base_dir, 'secrets.json'), 'rb') as secret_file:
            config_json = json.load(secret_file)
    except Exception as e:
        raise Exception(f"setting config error: {e}, {type(e).__name__}, {type(e)} [AT {base_dir}.settings]")

    if config_json is None:
        raise Exception(f"setting config error: 세팅 값이 NONE이 될 수 없습니다. [AT {base_dir}.settings]")

    return config_json