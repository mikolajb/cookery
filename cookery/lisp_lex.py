from ply.lex import TOKEN
import logging


class CookeryLexer(object):
    log = logging.getLogger("Cookery")

    keywords = ("let", "if", "car", "cdr", "require", "and", "or")

    tokens = [
        "EXP_BEGIN",
        "EXP_END",
        "FUNC",
        "ARG",
        "FLOAT",
        "INTEGER",
        "OPERATOR",
        "PATH",
        "STRING",
    ] + [k.upper() for k in keywords]

    states = (
        ('require', 'exclusive'),
    )

    def t_EXP_BEGIN(self, t):
        r'\('
        return t

    def t_EXP_END(self, t):
        r'\)'
        return t

    def t_ANY_REQUIRE(self, t):
        r'require'
        t.lexer.begin('require')
        return t

    def t_require_PATH(self, t):
        r'[\w\/_\.-]+'
        t.lexer.begin('INITIAL')
        return t

    def t_FUNC(self, t):
        r'[a-z_]+'
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
        return t

    def t_OPERATOR(self, t):
        r'[+\-\*/]'
        return t

    def t_ARG(self, t):
        r'[a-z_]+'
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
        return t

    def t_FLOAT(self, t):
        r'(?:[0-9]+\.[0-9]*)|(?:[0-9]*\.[0-9]+)'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'(?:[1-9]+[0-9]*)|0+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'(?:\'[^\']*\')|(?:"[^"]*")'
        return t

    t_ANY_ignore = ' \t'

    # t_ANY_ignore_COMMENT = r'\#.*'

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_ANY_error(self, t):
        self.log.warning("Illegal character '%s'" % t.value[0])
