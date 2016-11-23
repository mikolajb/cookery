class CookeryWrongMatch(Exception):
    pass


class CookeryWrongNumberOfArguments(Exception):
    pass


class CookeryCannotImportModule(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
