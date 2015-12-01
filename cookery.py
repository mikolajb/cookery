from cookery_parse import CookeryParser
from cookery_lex import CookeryLexer
from os import path, makedirs
import ply.yacc as yacc
import ply.lex as lex
import click


class Cookery:

    def __init__(self):
        self.lexer = lex.lex(module=CookeryLexer())
        self.parser = yacc.yacc(module=CookeryParser())

    def process_string(self, expression):
        t = self.parser.parse(expression, lexer=self.lexer)
        t.pretty_print()
        self.parser.restart()
        self.lexer.begin('INITIAL')
        for m in t.modules.keys():
            t.modules[m] = self.process_file(t.modules[m])
        return t

    def process_file(self, file):
        return self.process_string(file.read())

    def add_module(self, file, name):
        self.modules[name] = self.process_file(file)


@click.group()
@click.option('-c', '--config',
              type=click.File('r'),
              help='Config file.')
@click.option('--grammar_file',
              type=click.File('r'),
              help='Grammar file.')
@click.option('--print-config',
              is_flag=True,
              default=False,
              help='Prints configuration and exits without executing.')
@click.pass_context
def toolkit(ctx, config, grammar_file, print_config):
    print('toolkit', config, grammar_file, print_config)


@toolkit.command()
@click.argument('file', type=click.File('r'))
@click.pass_context
def run(ctx):
    'Executes a file.'
    print('rrrruuuun')


@toolkit.command()
@click.argument('expression')
@click.pass_context
def eval(ctx, expression):
    'Evaluates an expression.'
    c = Cookery()
    return c.process_string(expression)


@toolkit.command()
@click.argument('name')
@click.pass_context
def new(ctx, name):
    'Creates a new Cookery project.'
    print('new', ctx.parent.params)

    f_name = path.basename(name)

    if not path.exists(name):
        makedirs(name)

    empty_project = {
        '{}.py'.format(f_name):
        'action("test", :out) do |data|\n  puts "Just a test, passing data '
        'from subject"\n  data\nend\n\nsubject("Test", nil, "test") do\n  '
        '"fake result".bytes.map { |i| (i >= 97 and i <= 122 and rand > 0.5) '
        '? i - 32 : i }.pack("c*")\nend',
        '{}.cookery'.format(f_name): 'test Test.',
        '{}.toml'.format(f_name): '[actions.test]\njust_an_example = true',
    }

    for file, content in empty_project.items():
        with open(path.join(name, file), 'w') as f:
            f.write(content)


@toolkit.command()
@click.pass_context
def get(ctx):
    'Gets Cookery project from a repository.'
    print('getttt')

if __name__ == "__main__":
    toolkit()
    # lexer = lex.lex(module=CookeryLexer())
    # parser = yacc.yacc(module=CookeryParser())

    # expressions = [
    #     "do.",
    #     "do B.",
    #     "A = do B.",
    #     "do Aa and Bb.",
    #     "do {'a': 2}.",
    #     "do Aaa {'a': 2}.",
    #     '''create-email {"to"      : "mikolajb@gmail.com",
    #                  "from"    : "mikolajb@gmail.com",
    #                  "subject" : "Results",
    #                  "body"    : "Results for language test"}.''',
    #     'import "a/a" as b a.',
    #     'import \'b\' as b a.',
    #     '''import \'a\' as a
    #        import \'b\' as b
    #        d.''',
    #     'Test = read File.',
    #     'read with something.',
    #     'read.',
    #     'Test = read File with something.',
    #     'read File /tmp/test.txt.',
    #     'Test = read very http://example.com slowly File file:///tmp/test.txt with something.',
    #     'read very slowly.',
    #     'read very slowly with something.',
    #     'read very slowly with something else like this ftp://test.txt.',
    #     'Test = read File1 and File2 with something.',
    #     'Test = read File1 and File2[] and File3.',
    #     'Test = read File1 /tmp/test.txt and File2 with something.',
    #     'Test = read File1 /tmp/test.txt and File2 /tmp/test.aaa.',
    #     'T[] = read.',
    #     'read T[].'
    # ]

    # for expression in expressions:
    #     debug = False
    #     print("parsing:", expression)
    #     t = parser.parse(expression, lexer=lexer, debug=debug)
    #     t.pretty_print()
    #     parser.restart()
    #     lexer.begin('INITIAL')
