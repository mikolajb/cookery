from exceptions import NoImplementation


class Module:
    def __init__(self, imports, activities):
        self.imports = imports or []
        self.modules = {}
        for i in self.imports:
            self.modules[i['as']] = i['import']

        self.activities = activities or []
        self.variables = {}

    def execute(self, implementation, value=None):
        for a in self.activities:
            a.module = self
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
        self.subjects = []
        self.condition = None
        self.module = None

    def execute(self, implementation, value):
        subjects = []
        self.subjects
        for i in range(len(self.subjects)):
            if self.subjects[i].name in implementation.subjects:
                subjects.append(
                    implementation.subjects[self.subjects[i].name](
                        " ".join(self.subjects[i].arguments)
                    )
                )
            elif self.subjects[i].name in self.module.variables:
                subjects += self.module.variables[self.subjects[i].name]
            else:
                raise Exception()
        if self.condition:
            if self.condition.name not in implementation.conditions:
                raise NoImplementation()
            condition_func = implementation.conditions[self.condition.name]
            subjects = [condition_func(s) for s in subjects]
        if len(subjects) == 0 and value:
            subjects = value

        if self.action.name not in implementation.actions:
            if self.action.name in self.module.modules.keys():
                return self.module.modules[self.action.name]. \
                    execute(implementation, subjects)
            raise NoImplementation()

        if isinstance(self.action.arguments, list):
            self.action.arguments = " ".join(self.action.arguments)
        action_func = implementation.actions[self.action.name]
        result = action_func(subjects, self.action.arguments)
        if self.variable:
            self.module.variables[self.variable] = result
        return result

    def pretty_print(self):
        print('action:', self.action)
        print('condition:', self.condition)
        print('subjects:', len(self.subjects))
        if self.subjects:
            print('subjects:')
            for s in self.subjects:
                print(s)


class Action:
    def __init__(self, name, arguments=[]):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return self.name + ' ' + repr(self.arguments)


class Subject:
    def __init__(self, name, arguments=[]):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        return self.name + ' ' + repr(self.arguments)


class Condition:
    def __init__(self, name, arguments=[]):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        return self.name + ' ' + repr(self.arguments)
