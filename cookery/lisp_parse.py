from lisp_lex import CookeryLexer
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
    logging.basicConfig(level=logging.ERROR)
    tokens = CookeryLexer.tokens

    def p_forms(self, p):
        '''forms : form
                 | form forms'''

        p[0] = [p[1]]
        if len(p) > 2:
            p[0] += p[2]
        self.log.debug(p[0])

    def p_form(self, p):
        '''form : INTEGER
                | FLOAT
                | STRING
                | EXP_BEGIN proc_call EXP_END
                | EXP_BEGIN something EXP_END'''
                # | EXP_BEGIN progn forms EXP_END
        # if len(p) > 4:
        #     p[0] = p[3]
        if len(p) > 2:
            p[0] = p[2]
        else:
            p[0] = p[1]
        self.log.debug(p[0])

    def p_proc_call(self, p):
        '''proc_call : FUNC forms
                     | OPERATOR forms
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
        '''and_or : AND forms
                  | OR forms'''
        if p[1].upper() == "AND":
            p[0] = reduce(lambda i, acc: i and acc, p[2], True)
        elif p[1].upper() == "OR":
            p[0] = list(dropwhile(lambda i: not i, p[2]))[0]

    def p_require(self, p):
        '''require : REQUIRE PATH'''
        p[0] = p[1]

    def p_condition(self, p):
        '''condition : IF form form
                     | IF form form form'''
        self.log.debug("condition")
        if len(p) < 5:
            if p[2]:
                p[0] = p[3]
            else:
                p[0] = "aaa"
        else:
            if p[2]:
                p[0] = p[3]
            else:
                p[0] = p[4]

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
    (if 0 2 3)
    (if (+ 1 2) (- 10 20))
    2
    'a'
    (or "x" "y")
    """
    ,
    lexer=lexer,
    # debug=True
)

for l in x:
    print(l)
