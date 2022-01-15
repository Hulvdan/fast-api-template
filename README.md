# fast-api-template

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

### [poetry][PoetryLink]

На данный момент - это самый лучший менеджер Python пакетов.

Если вы не используете poetry... используйте poetry...

### Чистая архитектура

Особенность распространённых архитектурных подходов на любом языке
программирования заключается в том, что в центре ПО находится бизнес-логика,
а вокруг неё "плагинами" прикручивается всё остальное - веб-фреймворки, базы
данных, хранилища файлов, сервисы оповещений и т.п.

Данные подходы были выработаны индустрией для существенного облегчения
сопровождения проектов (в особенности - масштабирования), которые живут
несколько лет или десятилетий. За это время может смениться множество
технологий, могут появиться куда более привлекательные альтернативы,
но бизнес-логика... бизнес-логика не должна зависеть от технологий как можно
дольше, ведь хорошего архитектора от плохого отличает количество непринятых
решений.

Чистая архитектура не является исключением. В данном репозитории вы увидите
множественные примеры инверсии зависимостей, ограничения использования
бизнес-логикой внешних зависимостей посредством выстраивания слоёв абстракций
вокруг.

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

## Участие в проекте

### Первоначальная конфигурация после клонирования репозитория

Необходимо глобально установить pre-commit

```shell
pip install pre-commit
```

В папке проекта выполните следующую команду,
чтобы производились проверки перед каждым коммитом:

```shell
pre-commit install --install-hooks
pre-commit install --hook-type commit-msg
```

Настройка poetry для создания виртуальных окружений
внутри проектов в папках `.venv`.

```shell
poetry config virtualenvs.in-project true
```

```shell
cd backend
poetry install
```

[PreCommitLink]: https://commonmark.org/help/tutorial/07-links.html "pre-commit"
[BlackLink]: https://github.com/psf/black "Black"
[IsortLink]: https://github.com/PyCQA/isort "isort"
[MypyLink]: https://mypy.readthedocs.io/ "mypy"
[PoetryLink]: https://python-poetry.org/ "Poetry"
[PunqLink]: https://github.com/bobthemighty/punq "punq"
[DIConferenceLink]: https://www.youtube.com/watch?v=3Z_3yCgVKkM
