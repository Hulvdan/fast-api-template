###############################################################################
# --------------------------------- COMMON ---------------------------------- #
###############################################################################

# Цветной принт в консоль
highlight_color=$(shell echo -e "\033[0;34m")
success_color=$(shell echo -e "\033[0;32m")
default_color=$(shell echo -e "\033[0m")

define echo
@echo '$(highlight_color)$(1)$(default_color)'
endef

define echo_success
@echo '$(success_color)$(1)$(default_color)'
endef


###############################################################################
# --------------------------------- GENERAL --------------------------------- #
###############################################################################

# Заведение репозитория для разработки
init:: \
	pre-commit \
	upgrade-pyenv \
	backend

	@$(call echo_success,'Configured successfully!')

# Установка pre-commit
pre-commit::
	@$(call echo,'[general]: Installing pre-commit...')
	@pip install pre-commit --no-input
	@$(call echo,'[general]: Configuring pre-commit...')
	@pre-commit install --install-hooks
	@pre-commit install --hook-type commit-msg

# Обновление pyenv
upgrade-pyenv::
	@$(call echo,'[general]: Upgrading pyenv...')
	@cd $(HOME)/.pyenv && git pull && cd -


###############################################################################
# --------------------------------- BACKEND --------------------------------- #
###############################################################################

# Установка нужной версии python через pyenv и добавление в него poetry
backend-pyenv:: upgrade-pyenv
	@$(call echo,'[backend]: Installing python...')
	@pyenv install -s 3.10.2

	@$(call echo,'[backend]: Installing poetry...')
	@cd backend && pip install poetry --no-input

	@$(call echo,'[backend]: Configuring poetry...')
	@poetry config virtualenvs.in-project true

# Установка poetry
backend-poetry:: backend-pyenv
	@$(call echo,'[backend]: Initializing poetry...')
	@cd backend && poetry install

backend:: backend-poetry
