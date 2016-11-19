from .lisp_lex import CookeryLexer
import logging
from functools import reduce
from operator import sub, mul, truediv
from itertools import dropwhile
import ply.yacc as yacc
import ply.lex as lex

funs = {
    '+': sum,
    '-': lambda l: reduce(sub, l[1:], l[0]),
    '*': lambda l: reduce(mul, l[1:], l[0]),
    '/': lambda l: reduce(truediv, l[1:], l[0]),
    'test': lambda: "test"
}


class CookeryParser(object):

    log = logging.getLogger("CookeryParser")

    tokens = CookeryLexer.tokens

    def p_input(self, p):
        '''input : expressions'''
        p[0] = p[1]

    def p_expressions(self, p):
        '''expressions : expression
                       | pexpression
                       | expression expressions
                       | pexpression expressions'''
        p[0] = [p[1]]
        if len(p) > 2:
            p[0] += p[2]

    def p_pexpression(self, p):
        '''pexpression : EXP_BEGIN proc_call EXP_END
                       | EXP_BEGIN something EXP_END'''
        p[0] = p[2]

    def p_proc_call(self, p):
        '''proc_call : FUNC args
                     | OPERATOR args
                     | FUNC'''
        if len(p) > 2:
            p[0] = funs[p[1]](p[2])
            # p[0] = "{}({})".format(p[1], p[2])
        else:
            p[0] = funs[p[1]]()
            # p[0] = "{}".format(p[1])

    def p_something(self, p):
        '''something : require
                     | condition
                     | and_or'''

        p[0] = p[1]

    def p_and_or(self, p):
        '''and_or : AND expressions
                  | OR expressions'''
        if p[1].upper() == "AND":
            p[0] = reduce(lambda i, acc: i and acc, p[2], True)
        elif p[1].upper() == "OR":
            p[0] = list(dropwhile(lambda i: not i, p[2]))[0]

    def p_expression(self, p):
        '''expression : INTEGER
                      | FLOAT
        '''
        p[0] = p[1]

    def p_args(self, p):
        '''args : expression
                | expression args'''
        p[0] = [p[1]]
        if len(p) > 2:
            p[0] += p[2]

    def p_require(self, p):
        '''require : REQUIRE PATH'''
        p[0] = p[1]

    def p_condition(self, p):
        '''condition : IF pexpression pexpression
                     | IF pexpression expression
                     | IF expression expression
                     | IF expression pexpression
                     | IF expression expression expression
                     | IF expression pexpression expression
                     | IF pexpression expression expression
                     | IF expression expression pexpression
                     | IF expression pexpression pexpression
                     | IF pexpression expression pexpression
                     | IF pexpression pexpression expression
                     | IF pexpression pexpression pexpression'''
        if len(p) < 5:
            if p[2]:
                p[0] = p[3]
        else:
            p[0] = p[3] if p[2] else p[4]

    def p_error(self, p):
        if p:
            self.log.warning("Syntax error at '%s'" % p.value)
        else:
            self.log.debug("Syntax error at EOF")


lexer = lex.lex(module=CookeryLexer())
parser = yacc.yacc(module=CookeryParser())

x = parser.parse(
    """
    (- 10 2 1)
    (* 22.2 2 123 123123213 1111)
    (/ 100. 3)
    (+ 1 2 3)
    (and 1 2)
    (or 1 2)
    (if (+ 1 2) (- 10 20))
    (if 0 2 3)
    """,
    lexer=lexer,
    # debug=True
)

for l in x:
    print(l)
