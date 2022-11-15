class BaseException(Exception):
    def __init__(self, message):
        self.message = message

class NotFoundException(BaseException):
    pass
class AlreadyExistsException(BaseException):
    pass

class AccessDeniedException(BaseException):
    pass