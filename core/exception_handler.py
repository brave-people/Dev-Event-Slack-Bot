
# path setting
from os import path
import sys
sys.path.append(path.abspath('..'))

# custom lib
from logger import log


# 모든 이벤트를 받아서 처리하는 exception handerl
def exception_handler(exc):
    log(f"exception_handler : {exc}, {type(exc).__name__}, {type(exc)}")
    raise exc