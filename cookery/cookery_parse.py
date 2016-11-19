from .cookery_lex import CookeryLexer
import json
from .cookery_elements import Module, Activity, Action, Subject, Condition
import logging


class CookeryParser(object):

    log = logging.getLogger('Cookery')

    tokens = CookeryLexer.tokens

    def p_input(self, p):
        '''input : imports activities
                 | activities'''
        p[0] = Module(None, p[1]) if len(p) < 3 else Module(p[1], p[2])

    def p_imports(self, p):
        '''imports : IMPORT PATH AS MODULE
                   | IMPORT PATH AS MODULE imports'''
        p[0] = [{'import': p[2], 'as': p[4]}]
        if len(p) > 5:
            p[0] += p[5]

    def p_activities(self, p):
        '''activities : activity
                      | activity activities'''
        p[0] = [p[1]]
        if len(p) > 2:
            p[0] += p[2]

    def p_activity_1(self, p):
        'activity : action END'
        p[0] = Activity()
        p[0].action = p[1]

    def p_activity_2(self, p):
        'activity : action subject END'
        p[0] = Activity()
        p[0].action = p[1]
        p[0].subjects = p[2]

    def p_activity_3(self, p):
        '''activity : action IF condition END
                    | action WITH condition END'''
        p[0] = Activity()
        p[0].action = p[1]
        p[0].condition = p[3]

    def p_activity_4(self, p):
        '''activity : action subject IF condition END
                    | action subject WITH condition END'''
        p[0] = Activity()
        p[0].action = p[1]
        p[0].subjects = p[2]
        p[0].condition = p[4]

    def p_activity_5(self, p):
        'activity : VARIABLE "=" action END'
        p[0] = Activity()
        p[0].variable = p[1]
        p[0].action = p[3]

    def p_activity_6(self, p):
        'activity : VARIABLE "=" action subject END'
        p[0] = Activity()
        p[0].variable = p[1]
        p[0].action = p[3]
        p[0].subjects = p[4]

    def p_activity_7(self, p):
        '''activity : VARIABLE "=" action subject IF condition END
                    | VARIABLE "=" action subject WITH condition END'''
        p[0] = Activity()
        p[0].variable = p[1]
        p[0].action = p[3]
        p[0].subjects = p[4]
        p[0].condition = p[6]

    def p_action_1(self, p):
        'action : ACTION'
        p[0] = Action(p[1])

    def p_action_2(self, p):
        'action : ACTION action_arguments'
        p[0] = Action(p[1], p[2])

    def p_action_arguments_1(self, p):
        'action_arguments : JSON'
        p[0] = self._load_json(p[1])

    def p_action_arguments_2(self, p):
        'action_arguments : ACTION_ARGUMENT'
        p[0] = [p[1]]

    def p_action_arguments_3(self, p):
        'action_arguments : ACTION_ARGUMENT action_arguments'
        p[0] = [p[1]] + p[2]

    def p_subject_1(self, p):
        'subject : SUBJECT'
        p[0] = [Subject(p[1])]

    def p_subject_2(self, p):
        'subject : SUBJECT subject_arguments'
        p[0] = [Subject(p[1], p[2])]

    def p_subject_3(self, p):
        'subject : SUBJECT AND subject'
        p[0] = [Subject(p[1])]
        p[0] += p[3]

    def p_subject_4(self, p):
        'subject : SUBJECT subject_arguments AND subject'
        p[0] = [Subject(p[1], p[2])]
        p[0].append(p[4])

    def p_subject_arguments_1(self, p):
        'subject_arguments : JSON'
        p[0] = self._load_json(p[1])

    def p_subject_arguments_2(self, p):
        'subject_arguments : SUBJECT_ARGUMENT'
        p[0] = [p[1]]

    def p_subject_arguments_3(self, p):
        'subject_arguments : SUBJECT_ARGUMENT subject_arguments'
        p[0] = [p[1]] + p[2]

    def p_condition_1(self, p):
        'condition : CONDITION'
        p[0] = Condition(p[1])

    def p_condition_2(self, p):
        'condition : CONDITION condition_arguments'
        p[0] = Condition(p[1], p[2])

    def p_condition_arguments_1(self, p):
        'condition_arguments : JSON'
        p[0] = self._load_json(p[1])

    def p_condition_arguments_2(self, p):
        'condition_arguments : CONDITION_ARGUMENT'
        p[0] = [p[1]]

    def p_condition_arguments_3(self, p):
        'condition_arguments : CONDITION_ARGUMENT condition_arguments'
        p[0] = [p[1]] + p[2]

    def p_error(self, p):
        if p:
            self.log.warning("Syntax error at '%s'" % p.value)
        else:
            self.log.debug("Syntax error at EOF")

    def _load_json(self, data):
        self.log.debug('parsing JSON: {}'.format(data))
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError as e:
            self.log.warning('JSON syntax error {}'.format(e))
            return None
