# fast-api-template

[![Русский язык](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/bg.png) Русский язык](/README_ru.md)

## Rationale

I decided to create this project for enlightening purposes to spread
the application of good practices for running and maintaining a Python project.

## Best-practices, used in this project

### [pre-commit][PreCommitLink]

This framework makes it much easier to work with hooks in git.

It can be used to set up a number of commit quality checks -
ranging from formatting, linking, code validity,
to the messages of those commits.

### [black][BlackLink]

This is an uncompromising python file formatter, which in my opinion is better,
than the alternatives autopep8 and yapf.

I have not been able to get them to work together with isort,
so I have to live with black's PEP8 violations.

### [isort][IsortLink]

A tool for sorting imports in python files.

### [mypy][MypyLink]

A static code analyzer from the world of Python.
It allows you to use type annotations for premature code validation.

If there is invalid python code, for example:

```python
from typing import Any
def sum_str_and_int(string: str, number: int) -> Any:
    return string + number
```

Then mypy will generate the following error:

```bash
$ mypy .
a.py:3: error: Unsupported operand types for + ("str" and "int")
Found 1 error in 1 file (checked 1 source file)
```

If you take into account that mypy can be strictly customized,
you can be sure that the repository won't leak obviously broken code,
that the developer may have been careless.

In my practice, using mypy greatly reduces the number of such
errors during refactoring and reworking of existing functionality.

### [flake8][Flake8Link]

Flake8 is a linter. Linters help to keep the code consistent
and easy to understand. Flake8 functionality is extended by adding plugins
that introduce new code validation rules.

### [poetry][PoetryLink]

I'm a firm believer that at this moment **poetry**
is the best manager of python packages.

If you don't use poetry... use poetry...

### Clean Architecture

There were a lot of discussions about Clean Architecture.
I believe, this is a thing that every developer should know,
but don't be too fanatical about it.

### Dependency Injection

Dependency injection is an approach that allows an object
to receive other objects on which it depends at the design stage.

For some reason this approach is not actively used in Python projects,
although it is far from being a novelty in programming.

The [punq][PunqLink] library was chosen and slightly modified as a DI solution.

I made this decision after watching
a [presentation by Alexander Shibaev, Tinkoff][DIConferenceLink].
In it he reviewed the existing python libraries and frameworks,
that allow the use of DI and explained why they settled on **punq**.

## Further reading

You can enjoy the clean architecture
by navigating to the folder [backend](./backend)

## Development

### Initial configuration after cloning the repository

Configuration of the development environment
is performed with a single command: `make`.

It will install and configure **pre-commit**.

[PreCommitLink]: https://commonmark.org/help/tutorial/07-links.html "pre-commit"
[BlackLink]: https://github.com/psf/black "Black"
[IsortLink]: https://github.com/PyCQA/isort "isort"
[MypyLink]: https://mypy.readthedocs.io/ "mypy"
[Flake8Link]: https://github.com/pycqa/flake8 "flake8"
[PoetryLink]: https://python-poetry.org/ "Poetry"
[PunqLink]: https://github.com/bobthemighty/punq "punq"
[DIConferenceLink]: https://www.youtube.com/watch?v=3Z_3yCgVKkM
[PyenvSuggestedBuildEnvironment]: https://github.com/pyenv/pyenv/wiki#suggested-build-environment
[PyenvCommonBuildProblems]: https://github.com/pyenv/pyenv/wiki/Common-build-problems
