class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserDoesNotExistError(UserError):
    pass


class WrongPasswordError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class InvalidEmailError(UserError):
    pass
