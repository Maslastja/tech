VENV:= .venv
VENV_DIR:= $(VENV)/bin

# директории и файлы, которые необходимо исключить при проверке кода flake8
EXCL_PATH= .git,.venv,static,logs,.gitignore,__pycache__,.pytest_cache

help:
	@echo "Команды для управления проектом. Все команды (кроме env, clean) предполагают активированное виртуальное окружение "
	@echo "env         - создание виртуального окружения и установка пакетов из requirements/core.txt"
	@echo "env_up      - обновление виртуального окружения"
	@echo "env_prod    - установка пакетов prod-сервера из requirements/prod.txt"
	@echo "env_dev     - установка пакетов для отладки из requirements/dev.txt"
	@echo "env_list    - выводит на экран список установленных пакетов в виртуальное окружение"
	@echo "env_install - устанавливает/обновляет конкретный пакет в виртуальное окружение, необходимо указать параметр PACK_NAME"
	@echo "clean       - удаление кеша"
	@echo "test        - запуск тестов pytest"
	@echo "run         - запуск сервера (аналог flask run)"
	@echo "create_db   - создание таблиц при возможности подключения к БД"
	@echo "shell_db    - переход в консоль БД"
	@echo "flake       - запуск тестов flake8"
	@echo "prod        - полная установка приложения (env_prod create_db clean)"
	@echo "dev         - полная установка приложения для отладки (env_dev create_db clean)"

# очистка директорий проекта
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .pytest_cache`

# тестирование pytest
test: $(VENV) 
	@if ! [[ -f './.venv/bin/pytest' ]]; then\
		pip install pytest;\
	fi
	@PYTHONPATH=. pytest -v
	
# запуск сервера
run: $(VENV)
	@flask run

# создание БД и таблиц
create_db: $(VENV)
	@flask db create-all-tabs

# проверка flake8  
flake: $(VENV)
	@if ! [[ -f './.venv/bin/flake8' ]]; then\
		pip install flake8;\
	fi
	@flake8 --exclude=$(EXCL_PATH) .

# создание виртуального окружения и установка пакетов
env: requirements/core.txt
	@python3 -m venv $(VENV)
	@$(VENV_DIR)/pip install -r requirements/core.txt 

# загрузка пакетов prod
env_prod: $(VENV) requirements/prod.txt
	@pip install -r requirements/prod.txt
	
# загрузка пакетов dev
env_dev: $(VENV) requirements/dev.txt
	@pip install -r requirements/dev.txt

# обновление пакетов виртуального окружения
env_up: $(VENV)
	@pip install --upgrade pip
	@pip install --upgrade setuptools
	@pip install --upgrade wheel

# вывод списка установленных пакетов
env_list: $(VENV)
	@pip list

# установка/обновление пакетов
env_install: $(VENV)
	@if [ "${PACK_NAME}" ]; then\
		pip install $(PACK_NAME) --upgrade;\
	else\
		echo 'необходимо указать название пакета: make pip_install PACK_NAME=*name*';\
	fi
	
# полная установка приложения (виртаульное окружение, база данных)
prod: env_prod create_db clean

dev: env_dev create_db clean

# запуск консоли базы данных
shell_db: $(VENV)
	flask db shell-db

.PHONY: help clean run test env	
	
