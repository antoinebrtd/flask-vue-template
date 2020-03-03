from {{cookiecutter.project_name}}.exceptions import APIError


class PasswordError(APIError):
    def __init__(self, message, status_code=None):
        APIError.__init__(self, 'Passwords', message, status_code)


class EmailPasswordMismatch(PasswordError):
    def __init__(self):
        PasswordError.__init__(self, "Wrong password", 400)


class PasswordRequired(PasswordError):
    def __init__(self):
        PasswordError.__init__(self, "Password is required", 400)


class PasswordTooShort(PasswordError):
    def __init__(self):
        PasswordError.__init__(self, "Min 8 characters", 400)


class SamePasswords(PasswordError):
    def __init__(self):
        PasswordError.__init__(self, "Old password and new password must be different", 400)
