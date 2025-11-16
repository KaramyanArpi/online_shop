class AppException(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class InvalidInputError(AppException):
    def __init__(self, field1="username", field2="age"):
        msg = f"Invalid input! Insert correct values for {field1} and {field2}"
        super().__init__(msg, status_code=400)

class NotFoundError(AppException):
    def __init__(self, entity="Item", field="id", value=None):
        msg = f"{entity} with {field} '{value}' not found"
        super().__init__(msg, status_code=404)

class AlreadyExistsError(AppException):
    def __init__(self, field_name, value):
        message = f"{field_name} '{value}' already exists"
        super().__init__(message, status_code=409)


class ValidationError(AppException):
    def __init__(self, message):
        super().__init__(message, status_code=400)


class DatabaseError(AppException):
    def __init__(self, message="Database operation failed"):
        super().__init__(message, status_code=500)

