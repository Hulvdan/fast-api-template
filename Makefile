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
init:: pre-commit

	@$(call echo_success,'Configured successfully!')

# Установка pre-commit
pre-commit::
	@$(call echo,'[general]: Installing pre-commit...')
	@pip install pre-commit --no-input
	@$(call echo,'[general]: Configuring pre-commit...')
	@pre-commit install --install-hooks
	@pre-commit install --hook-type commit-msg
