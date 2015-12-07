from exceptions import NoImplementation
import logging

class Module:
    def __init__(self, imports, activities):
        self.log = logging.getLogger('Cookery')
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
        res = ""
        res += 'imports:\n'
        for i in self.imports:
            res += '- {}'.format(i)
        for a in self.activities:
            res += a.pretty_print()
        return res


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
        res = '''action: {}
condition: {}
subjects: {}'''.format(self.action,
                       self.condition,
                       len(self.subjects))
        if self.subjects:
            res += 'subjects:'
            for s in self.subjects:
                res += str(s)
        return res


class Element:
    def __init__(self, name, arguments=[]):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return '{}({})'.format(self.name, repr(self.arguments))


class Action(Element):
    pass


class Subject(Element):
    pass


class Condition(Element):
    pass
