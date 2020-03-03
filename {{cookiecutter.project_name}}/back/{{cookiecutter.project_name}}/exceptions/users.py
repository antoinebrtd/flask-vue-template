from {{cookiecutter.project_name}}.exceptions import APIError


class UserError(APIError):
    def __init__(self, message, status_code=None):
        APIError.__init__(self, 'Users', message, status_code)


class EmailAddressAlreadyTaken(UserError):
    def __init__(self):
        UserError.__init__(self, 'An account with this email address already exists', 401)


class UserNotFound(UserError):
    def __init__(self):
        UserError.__init__(self, 'No account associated with this email address', 404)


class InvalidLink(UserError):
    def __init__(self):
        UserError.__init__(self, "This link is invalid or has expired", 404)


class AccountAlreadyActivated(UserError):
    def __init__(self):
        UserError.__init__(self, "Your account is already activated", 403)


class EmailRequired(UserError):
    def __init__(self):
        UserError.__init__(self, "Email is required", 400)


class FirstNameRequired(UserError):
    def __init__(self):
        UserError.__init__(self, "First name is required", 400)


class LastNameRequired(UserError):
    def __init__(self):
        UserError.__init__(self, "Last name is required", 400)


class EmailNotConfirmed(UserError):
    def __init__(self):
        UserError.__init__(self, "An account with this email address already exists and hasn't been activated", 401)
