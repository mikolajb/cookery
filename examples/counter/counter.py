@cookery.action()
def split(subjects):
    return subjects[0].split()

@cookery.action()
def count(subjects):
    return len(subjects[0])

@cookery.subject('in', r'(.+)')
def file(path):
    print('opening file:', repr(path))
    f = open(path, 'r')
    return f.read()
