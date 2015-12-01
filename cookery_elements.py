class Module:
    def __init__(self, imports, activities):
        self.imports = imports or []
        self.modules = {}
        for im_path, im_name in self.imports:
            self.modules[im_name] = im_path

        self.activities = activities or []

    def execute(self, implementation, value):
        for a in self.activities:
            value = a.execute(implementation, value)
        return value

    def pretty_print(self):
        print('imports:')
        for i in self.imports:
            print(i)
        for a in self.activities:
            a.pretty_print()


class Activity:
    def __init__(self):
        self.variable = None
        self.action = None
        self.subjects = None
        self.condition = None

    def execute(self, implementation, value):
        return implementation['actions'][self.action.name](value)

    def pretty_print(self):
        print('action:', self.action)
        print('condition:', self.condition)
        if self.subjects:
            print('subjects:')
            for s in self.subjects:
                print(s)


class Action:
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return self.name + ' ' + repr(self.arguments)


class Subject:
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        return self.name + ' ' + repr(self.arguments)


class Condition:
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        return self.name + ' ' + repr(self.arguments)
