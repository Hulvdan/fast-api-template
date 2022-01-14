# fast-api-template

Здесь собраны лучшие практики ведения проекта

## Contributing to the project

### pre-commit

Необходимо глобально установить pre-commit

```shell
pip install pre-commit
```

В папке проекта выполните следующую команду, чтобы производились проверки перед каждым коммитом:

```shell
pre-commit install --install-hooks
pre-commit install --hook-type commit-msg
```

### poetry

```shell
poetry config virtualenvs.in-project true
```

```shell
cd backend
poetry install
```
