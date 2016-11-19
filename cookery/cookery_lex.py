from ply.lex import TOKEN
import logging


class CookeryLexer(object):

    log = logging.getLogger('Cookery')

    keywords = ('import', 'and', 'if', 'with', 'as')

    tokens = [
        'PATH',
        'MODULE',
        'VARIABLE',
        'ACTION',
        'ACTION_ARGUMENT',
        'SUBJECT',
        'SUBJECT_ARGUMENT',
        'CONDITION',
        'CONDITION_ARGUMENT',
        'JSON',
        'END'
    ] + [k.upper() for k in keywords]

    states = (
        ('import', 'exclusive'),
        ('importmodule', 'exclusive'),
        ('subject', 'exclusive'),
        ('subjectargument', 'exclusive'),
        ('condition', 'exclusive'),
        ('conditionargument', 'exclusive'),
    )

    def t_ANY_IMPORT(self, t):
        r'import'
        t.lexer.begin('import')
        return t

    import_path = r'[\w\/_\.-]+'
    wrapped_path = r'(\'' + import_path + r'\')|' + \
                   r'(\"' + import_path + r'\")|' + \
                   r'(' + import_path + ')'

    @TOKEN(wrapped_path)
    def t_import_PATH(self, t):
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
        else:
            t.value = t.value.strip("'").strip('"')
            t.lexer.begin('importmodule')
        return t

    def t_importmodule_MODULE(self, t):
        r'\w+'
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
        else:
            t.lexer.begin('INITIAL')
        return t

    def t_INITIAL_VARIABLE(self, t):
        r'[A-Z][\w_-]*(\[\])?'
        return t

    def t_INITIAL_ACTION(self, t):
        r'[a-z][\w_-]*'
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
        else:
            t.lexer.begin('subject')
        return t

    def t_subject_ACTION_ARGUMENT(self, t):
        r'[^A-Z{\.](:?(?!(:?\.\s)|(:?\.\Z))[^ ])*'
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
            if t.type in ['IF', 'WITH']:
                t.lexer.begin('condition')
        return t

    def t_subject_SUBJECT(self, t):
        r'[A-Z][\w_-]*(\[\])?'
        t.lexer.begin('subjectargument')
        return t

    def t_subjectargument_SUBJECT_ARGUMENT(self, t):
        r'(:?(?!(:?\.\s)|(:?\.\Z))[^ {])+'
        if t.value in CookeryLexer.keywords:
            t.type = t.value.upper()
            if t.type in ['IF', 'WITH']:
                t.lexer.begin('condition')
            elif t.type == 'AND':
                t.lexer.begin('subject')
        return t

    def t_condition_CONDITION(self, t):
        r'[a-z][\w_-]*'
        t.lexer.begin('conditionargument')
        return t

    def t_conditionargument_CONDITION_ARGUMENT(self, t):
        r'(:?(?!(:?\.\s)|(:?\.\Z))[^ {])+'
        return t

    def t_ANY_END(self, t):
        r'\.'
        t.lexer.begin('INITIAL')
        return t

    t_ANY_JSON = r'{[^}]+}'

    literals = ('=')

    t_ANY_ignore = ' \t'
    t_ANY_ignore_COMMENT = r'\#.*'

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_ANY_error(self, t):
        self.log.warning("Illegal character '%s'" % t.value[0])
