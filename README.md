# Cookery #

## Features

- Integration with Jupyter Notebook
- connect to cloud
- another example with services
- three layers of Cookery
  - guideline for users
  - guideline for developers
  - example on how to implement the lower layer
  - ask Kasia what happened with this student
  - write something

## Video

Cookery is a framework for designing Domain Specific Languages for scientific applications in a cloud environment.

## How to install ##

You will need to use Python3. I tested it with version 3.6.

Clone the repository:

```
git clone https://github.com/mikolajb/cookery.git
```

and install using pip

```
pip install --user .  # be sure to use the one associated with python3 (pip3?)
```

### Integration with Jupyter Notebook

If you have a Jupyter Notebook installed in your system, you can take the advantage from Cookery kernel which is supplied with cookery. You can register a kernel with a command:

```
cookery kernel
```

Then, if you start `jupyter notebook`, you can select "Cookery" as a kernel and execute Cookery scripts in a browser.

## How to use ##

First, without creating any files, you can evaluate cookery expressions in the following way:

```
cookery eval "echo 'Hello world!'."
```

### Creating a new project ###

Using a toolkit, you can create a project in a following way:

```
cookery new PROJECT_NAME
```

Then, it can be immediately evaluated using:

```
cookery run PROJECT_NAME/test.cookery
```

## How does it work ##

Cookery is inspired by cooking recipes and it allows to develop scientific applications with plain English. Applications are build from a number of sentences (_activities_) which, in turn consist the following components:

1. Action (always one)
1. Condition (zero or many)
1. Subject (zero or many)

A result of every _activity_ can be stored in a _variable_ and then used in other _activity_ as a _subject_.


### Action ###

__Action__ is a pair: __name__ (starts with a __lowercase__ letter) and _procedure_. Name_ is a reference to created action and can be used in a place of `action` (see syntax). _Procedure_ is a block of code that takes one argument - _subject_. During the execution, _action_ receives a reference to a _subject_ specified be a user.

### Condition ###

__Condition__ is very similar to _action_. It has a __name__ (starts with a lowercase) and __procedure__. They should have longer, descriptive names and be designed in a way that can work well with various _actions_.

### Subject ###

__Subject__ is built from four elements: __name__ (starts with __uppercase__ letter), __type__, __regular expression__ and __procedure__.

- _name_ is a reference to subject's procedure
- _regular expression_ is used to parse subject's arguments, all elements captured by a regular expression are available as arguments
- _type_ (or protocol) points to an implementation of subject's backend, backend provides methods that can be used in a _procedure_ to specify protocol's parameters (e.g. _path_)
- _procedure_ - block of Ruby code where all the parameters specific to a protocol can be specified using functions provided by a protocol implementation

### Syntax ###

These components define named entities - keywords that can be used in a following syntax:

    action Subject [arguments] - condition condition ... condition.

### Example ###

In a following example we show an application that counts words in a file.

First, we create a new project:

    cookery new counter

Then, all the required components have to be defined in `counter.py` file:

```
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
```

It is important to note, that _action_ receives a _subject_ data in a list, even if there is only one _subject_.

File `counter.cookery` should contain Cookery language that uses defined _actions_ and _subjects_:

```
A = split File text_file.txt.
count A.
```
