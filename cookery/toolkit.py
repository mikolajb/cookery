import click
from os import path, makedirs
from .cookery import Cookery
import ply.yacc as yacc
import ply.lex as lex
from .cookery_lex import CookeryLexer
from .cookery_parse import CookeryParser
import json


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
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Runs Cookery in debug mode')
@click.option('--debug-lexer',
              is_flag=True,
              default=False,
              help='Runs lexer in debug mode')
@click.option('--debug-parser',
              is_flag=True,
              default=False,
              help='Runs parser in debug mode')
@click.pass_context
def toolkit(ctx,
            config,
            grammar_file,
            print_config,
            debug,
            debug_lexer,
            debug_parser):
    ctx.obj = {}
    ctx.obj['debug'] = debug
    ctx.obj['debug_lexer'] = debug_lexer
    ctx.obj['debug_parser'] = debug_parser


@toolkit.command()
@click.argument('file', type=click.File('r'))
@click.pass_context
def run(ctx, file):
    'Executes a file.'
    cookery = Cookery(ctx.parent.params['debug'],
                      ctx.parent.params['debug_lexer'],
                      ctx.parent.params['debug_parser'])
    print('returned value:', cookery.execute_file(file))


@toolkit.command()
@click.argument('expression')
@click.pass_context
def eval(ctx, expression):
    'Evaluates an expression.'
    c = Cookery(**ctx.obj)
    click.echo(c.execute_expression(expression))


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
        "from random import randint\n"
        "\n"
        "@cookery.action()\n"
        "def test(subject):\n"
        "    print(\"Just a test, passing data from subject.\")\n"
        "    return subject\n"
        "\n"
        "@cookery.subject(\"in\")\n"
        "def test():\n"
        "    return \"\".join(map(lambda i: randint(0, 1) and i.upper() or i,"
        "\n"
        "                       \"fake result\"))\n",
        '{}.cookery'.format(f_name): 'test Test.',
        '{}.toml'.format(f_name): '[actions.test]\njust_an_example = true',
    }

    for file, content in empty_project.items():
        with open(path.join(name, file), 'w') as f:
            f.write(content)


@toolkit.command()
@click.option('--uninstall',
              is_flag=True,
              default=False,
              help='Uninstall Cookery Jupyter kernel.')
@click.pass_context
def kernel(ctx, uninstall):
    'Install Jupyter kernel'
    import jupyter_client

    kernel_path = path.join(
        path.dirname(path.abspath(__file__)),
        "cookerykernel",
    )
    ksm = jupyter_client.kernelspec.KernelSpecManager()

    if uninstall:
        ksm.remove_kernel_spec("cookery")
    else:
        ksm.install_kernel_spec(
            kernel_path,
            kernel_name="cookery",
            user=True,
        )

@toolkit.command()
@click.pass_context
def get(ctx):
    'Gets Cookery project from a repository.'
    print('getttt')


@toolkit.command()
def test():
    lexer = lex.lex(module=CookeryLexer())
    parser = yacc.yacc(module=CookeryParser())

    expressions = [
        "do.",
        "do B.",
        "A = do B.",
        "do Aa and Bb.",
        "do {'a': 2}.",
        "do Aaa {'a': 2}.",
        '''create-email {"to"      : "mikolajb@gmail.com",
                     "from"    : "mikolajb@gmail.com",
                     "subject" : "Results",
                     "body"    : "Results for language test"}.''',
        'import "a/a" as b a.',
        'import \'b\' as b a.',
        '''import \'a\' as a
           import \'b\' as b
           d.''',
        'Test = read File.',
        'read with something.',
        'read.',
        'Test = read File with something.',
        'read File /tmp/test.txt.',
        '''Test = read very http://example.com slowly File
          file:///tmp/test.txt with something.''',
        'read very slowly.',
        'read File with test.',
        'read very slowly with something.',
        'read very slowly with something else like this ftp://test.txt.',
        'Test = read File1 and File2 with something.',
        'Test = read File1 and File2[] and File3.',
        'Test = read File1 /tmp/test.txt and File2 with something.',
        'Test = read File1 /tmp/test.txt and File2 /tmp/test.aaa.',
        'T[] = read.',
        'read T[].',
        'do File. do File. do File.',
    ]

    for expression in expressions:
        debug = False
        print('--------------------------------------------------')
        print("parsing:", expression)
        print()
        t = parser.parse(expression, lexer=lexer, debug=debug)
        print(t.pretty_print())
        parser.restart()
        lexer.begin('INITIAL')


if __name__ == "__main__":
    toolkit()
