from typing import Literal

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
    
class TokenException(AppException):
    def __init__(self, message: str, token_type: Literal["access", "refresh"]):
        self.message = message
        self.token_type = token_type
        super().__init__(message)

class ReportException(AppException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)

class FoundExceptionLLM(AppException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)

class DecryptException(AppException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)

class EncryptException(AppException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)

class ExistingReportException(AppException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)