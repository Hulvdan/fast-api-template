# fast-api-template

[![English Language](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/us.png) English Language](/README_ru.md)

## Мотивация

Я решил создать данный проект в просветительских целях для распространения
применения хороших практик ведения проекта на Python и поддержании его
архитектуры.

## "Best"-практики, использованные в данном проекте

### [pre-commit][PreCommitLink]

Данный фреймворк значительно облегчает работу с хуками в git.

С его помощью можно настроить ряд проверок качества коммитов -
начиная от форматирования, линтинга, валидности кода,
заканчивая сообщениями этих коммитов.

### [black][BlackLink]

Это бескомпромиссный форматтер python-файлов, который по моему мнению лучше,
чем другие альтернативы - autopep8 и yapf.

У меня не получилось на своём опыте подружить их вместе с isort, поэтому
приходится мириться с нарушениями PEP8 по вине black и довольствоваться
лишь однородным форматированием кода.

### [isort][IsortLink]

Инструмент для умного сортирования импортов в python-файлах.

### [mypy][MypyLink]

Статический анализатор кода из мира Python. Он позволяет использовать
аннотации типов для преждевременной проверки работоспособности кода.

Если в репозитории будет невалидный python-код, например:

```python
from typing import Any
def sum_str_and_int(string: str, number: int) -> Any:
    return string + number
```

То mypy выдаст следующую ошибку:

```bash
$ mypy .
a.py:3: error: Unsupported operand types for + ("str" and "int")
Found 1 error in 1 file (checked 1 source file)
```

Если принять во внимание, что mypy можно строжайше настроить, то можно быть
уверенным в том, что в репозиторий не прольётся очевидно неработающий код,
который разработчик мог допустить по невнимательности.

На моей практике использование mypy значительно уменьшает количество таких
ошибок во время рефакторинга и переработок существующего функционала.

### [flake8][Flake8Link]

Flake8 - линтер. Линтеры помогают поддерживать код однородным и легким для
восприятия. Функционал Flake8 расширяется путём добавления плагинов,
которые вносят новые правила проверки кода.

### [poetry][PoetryLink]

На данный момент - это самый лучший менеджер Python пакетов.

Если вы не используете poetry... используйте poetry...

### Чистая архитектура

Много дискуссий было по поводу Чистой Архитектуры.
Я считаю, что это то, что должен знать каждый разработчик,
но использовал не из фанатичных побуждений.

### Dependency Injection - Внедрение зависимостей

Внедрение зависимостей - это подход, позволяющий объекту получать
другие объекты, от которых он зависит, на этапе конструирования.

Данный подход почему-то не очень активно используется в Python проектах, хотя
он - далеко не новшество в программировании.

В качестве DI решения была выбрана и
слегка допилена библиотека [punq][PunqLink].

Данное решение мною было принято после просмотра
[выступления][DIConferenceLink] Александра Шибаева, Тинькофф.
В нём он рассмотрел существующие python-библиотеки и фреймворки,
позволяющие использовать DI и объяснил, почему они остановились на punq.

## Далее

Вы можете преисполниться чистой архитектурой,
перейдя в папку [backend](./backend)

## Разработка

### Первоначальная конфигурация после клонирования репозитория

Конфигурация окружения для разработки выполняется одной командой: `make`.

Это установит и настроит **pre-commit**.

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
