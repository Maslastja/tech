VENV_DIR:= .venv
PATH:= $(VENV_DIR)/bin:$(PATH)
FLASK_CREATE_DB:= db create-all-tabs 
FLASK_SHELL_DB:= db shell-db 

# директории и файлы, которые необходимо исключить при проверке кода flake8
EXCL_PATH= .git,.venv,static,logs,.gitignore,__pycache__,.pytest_cache

help:
	@echo "Команды для управления проектом"
	@echo "env         - создание виртуального окружения и установка пакетов из requirements/core.txt"
	@echo "env_up      - обновление виртуального окружения"
	@echo "env_prod    - установка пакетов prod-сервера из requirements/prod.txt"
	@echo "env_dev     - установка пакетов для отладки из requirements/dev.txt"
	@echo "clean       - удаление кеша"
	@echo "test        - запуск тестов pytest"
	@echo "run         - запуск сервера (аналог flask run)"
	@echo "create_db   - создание таблиц при возможности подключения к БД"
	@echo "shell_db    - переход в консоль БД"
	@echo "flake       - запуск тестов flake8"
	@echo "prod        - полная установка приложения (env env_prod create_db clean)"
	@echo "dev         - полная установка приложения для отладки (env env_dev create_db clean)"

# очистка директорий проекта
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .pytest_cache`

# тестирование pytest
test: $(VENV_DIR) 
	@if ! [[ -f './.venv/bin/pytest' ]]; then\
		pip install pytest;\
	fi
	@PYTHONPATH=. pytest -v
	
# запуск сервера
run: env create_db 
	@flask run

# создание БД и таблиц
create_db: $(VENV_DIR)
	@flask $(FLASK_CREATE_DB)

# проверка flake8  
flake: $(VENV_DIR)
	@if ! [[ -f './.venv/bin/flake8' ]]; then\
		pip install flake8;\
	fi
	@flake8 --exclude=$(EXCL_PATH) .

# создание виртуального окружения и установка пакетов
env: requirements/core.txt
	@python3 -m venv $(VENV_DIR)
	@pip install -Ur requirements/core.txt 

# загрузка пакетов prod
env_prod: $(VENV_DIR) requirements/prod.txt
	@pip install -Ur requirements/prod.txt
	
# загрузка пакетов dev
env_dev: $(VENV_DIR) requirements/dev.txt
	@pip install -Ur requirements/dev.txt

# обновление пакетов виртуального окружения
env_up: $(VENV_DIR)
	@pip install --upgrade pip
	@pip install --upgrade setuptools
	@pip install --upgrade wheel
	
# полная установка приложения (виртаульное окружение, база данных)
prod: env env_prod create_db clean

dev: env env_dev create_db clean

# запуск консоли базы данных
shell_db: $(VENV_DIR)
	@flask $(FLASK_SHELL_DB)

.PHONY: help clean run test env	
	
