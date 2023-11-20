from pydantic import ValidationError

ValidatorException = ValidationError


class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    def __init__(self):
        super().__init__("template not found")


class InternalServiceException(ServiceException):
    pass
