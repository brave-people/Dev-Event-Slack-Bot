
# custom lib
from core.db.mongodb import Repository


def exception_handler(exc, repository: Repository):
    '''
    모든 이벤트를 받아서 처리하는 exception handerl
    '''
    repository.log_data("error_log", f"exception_handler : {exc}, {type(exc).__name__}, {type(exc)}")
    raise exc