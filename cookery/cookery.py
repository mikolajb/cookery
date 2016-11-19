from .cookery_parse import CookeryParser
from .cookery_lex import CookeryLexer
from functools import wraps
from os import path, listdir
import ply.yacc as yacc
import ply.lex as lex
import runpy
import re
import inspect
import logging
from operator import methodcaller
from .exceptions import \
    WrongMatch, \
    WrongNumberOfArguments, \
    CannotImportModule


class Cookery:
    STDLIB_PATH = 'stdlib'

    def __init__(self, debug=False, debug_lexer=False,
                 debug_parser=False, jupyter=False):
        if not jupyter:
            self.init_logging(debug)
        self.lexer = lex.lex(module=CookeryLexer(), debug=debug_lexer)
        self.debug_parser = debug_parser
        self.parser = yacc.yacc(module=CookeryParser())
        self.subjects = {}
        self.actions = {}
        self.conditions = {}
        stdlib_path = path.join(path.dirname(path.abspath(__file__)),
                                self.STDLIB_PATH)
        for f in filter(methodcaller('endswith', '.py'),
                        listdir(stdlib_path)):
            self.process_implementation(path.join(stdlib_path, f))

    def init_logging(self, debug):
        self.log = logging.getLogger('Cookery')
        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def process_expression(self, expression):
        m = self.parser.parse(expression,
                              lexer=self.lexer,
                              debug=self.debug_parser)
        self.log.debug('module: {}'.format(m.pretty_print()))
        self.parser.restart()
        self.lexer.begin('INITIAL')
        self.process_imports(m)
        self.log.debug('imports: {}'.format(m.modules))
        return m

    def process_imports(self, module):
        for m in module.modules.keys():
            module.modules[m] = self.load_module(module.modules[m])
            self.process_imports(module.modules[m])

    def process_file(self, file):
        "Processes Cookery file"
        if isinstance(file, str):
            name, ext = path.splitext(file)
            if ext == '' or ext == '.cookery':
                file = name + '.cookery'
                if path.exists(file):
                    file = open(file, 'r')
                else:
                    raise CannotImportModule
            else:
                raise CannotImportModule
        return self.process_expression(file.read())

    def process_implementation(self, file):
        "Processes Cookery middleware file"
        implementation = path.splitext(
            file if isinstance(file, str) else file.name)[0] + '.py'
        if path.exists(implementation):
            runpy.run_path(implementation, {'cookery': self})
        else:
            raise NotImplementedError()

        return implementation

    def load_module(self, file):
        module = self.process_file(file)
        self.process_implementation(file)
        return module

    def execute_file(self, file):
        module = self.load_module(file)
        return module.execute(self)

    def execute_expression(self, expression):
        module = self.process_expression(expression)
        return module.execute(self)

    def execute_expression_interactive(self, expression):
        module = self.process_expression(expression)
        if not hasattr(self, 'state'):
            self.state = None
        self.state = module.execute(self, self.state)
        return self.state

    def complete(self, expression):
        'Completes the code, todo: complete words, not only tokens.'

        self.parser.parse(expression, lexer=self.lexer)
        self.log.debug('complete action: {}'.format(self.parser.action))
        self.log.debug('complete statestack: {}'.format(self.parser.statestack))
        self.log.debug('complete symstack: {}'.format(self.parser.symstack))
        stack = self.parser.symstack[-1]
        self.log.debug('stack: {}'.format(stack))
        if stack not in ['include', '$end']:
            action = self.parser.action[self.parser.statestack[-1]]
            possibilities = action.keys()
            self.log.debug("possibilities are: {}".format(possibilities))
            result = list(map(methodcaller('lower'),
                              set(possibilities) &
                              set(['IMPORT', 'AND', 'AS', '='])))

            if len(self.conditions) > 0:
                result += list(map(methodcaller('lower'),
                                   set(possibilities) &
                                   set(['IF', 'WITH'])))

            if len(expression) > 0:
                if not re.match(r'\s', expression[-1]):
                    if 'END' in possibilities:
                        return [' ', '.']
                    else:
                        return [' ']

            for p in possibilities:
                if p == 'ACTION':
                    result += self.actions.keys()
                elif p == 'SUBJECT':
                    result += self.subjects.keys()
                elif p == 'CONDITION':
                    result += self.conditions.keys()
                # elif p == 'JSON':
                #     result +=
                # elif p == 'ACTION_ARGUMENT':
                #     result +=
                # elif p == 'SUBJECT_ARGUMENT':
                #     result +=
                # elif p == 'CONDITION_ARGUMENT':
                #     result +=
            return result
        self.parser.restart()
        self.lexer.begin('INITIAL')
        return ""

    def subject(self, type, regexp=None):
        def decorator(func):
            @wraps(func)
            def wrapper(arguments):
                if regexp == 'JSON':
                    return func(arguments)
                matched = re.match(regexp, arguments)
                if matched:
                    return func(*matched.groups())
                else:
                    pass  # handle unmached data
                return func()
            # changes func name from foo_bar to FooBar
            func_name = "".join([e.capitalize() for e in
                                 func.__name__.split('_')])
            self.subjects[func_name] = wrapper
            return wrapper
        return decorator

    def action(self, regexp=None):
        def decorator(func):
            @wraps(func)
            def wrapper(subjects=None, arguments=None):
                parameters = len(inspect.signature(func).parameters)

                if regexp == 'JSON':
                    if parameters == 1:
                        return func(arguments)
                    elif parameters == 2:
                        return func(subjects, arguments)
                    else:
                        raise WrongNumberOfArguments()
                if regexp:
                    matched = re.match(regexp, arguments)
                    if matched:
                        if parameters == 1 + len(matched.groups()):
                            return func(subjects, *matched.groups())
                        else:
                            raise WrongNumberOfArguments()
                    else:
                        raise WrongMatch()
                return func(subjects, *([None] * (parameters - 1)))
            self.actions[func.__name__] = wrapper
            return wrapper
        return decorator

    def condition(self, regexp=None):
        def decorator(func):
            @wraps(func)
            def wrapper(value, arguments):
                if regexp == 'JSON':
                    return func(value, arguments)
                if regexp:
                    matched = re.match(regexp, arguments)
                    if matched:
                        return func(value, *matched.groups())
                    else:
                        pass  # handle unmached data
                return func(value)
            self.conditions[func.__name__] = func
            return wrapper
        return decorator
