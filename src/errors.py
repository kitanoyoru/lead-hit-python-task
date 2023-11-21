class ServiceException(Exception):
    pass


class ValidatorException(ServiceException):
    def __init__(self, msg: str):
        super().__init__(msg)


class NotFoundException(ServiceException):
    def __init__(self):
        super().__init__("template not found")


class InternalServiceException(ServiceException):
    pass
