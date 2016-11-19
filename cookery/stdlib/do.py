@cookery.action('')
def do(subject):
    print('in do action with subject:', subject)
    return subject

@cookery.action('(.*)')
def echo(subject, text):
    return text

@cookery.subject('in', r'(.+)')
def file(path):
    print('opening file:', repr(path))
    f = open(path, 'r')
    return f.read()
