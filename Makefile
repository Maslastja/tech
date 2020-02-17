ROOT_DIR:= .
PYTHONPATH:= .
VENV_DIR:= $(ROOT_DIR)/.venv/env/bin
PIP_DIR:= $(VENV_DIR)/pip
PYTHON_DIR:= $(VENV_DIR)/python
FLASK_DIR:= $(VENV_DIR)/flask
FLAKE_DIR:= $(VENV_DIR)/flake8
PYTEST_DIR:= $(VENV_DIR)/pytest
ACTIVATE_ENV:= . $(VENV_DIR)/activate

# команда создания таблиц в БД
COMMAND_BD= db create-all-tabs

# директории и файлы, которые необходимо исключить при проверке кода flake8
EXCL_PATH= .git,.venv,static,logs,.gitignore,__pycache__

help:
	@echo "clean 	- удаление кеша"
	@echo "test 	- запуск тестов pytest"
	@echo "run 	- запуск сервера"
	@echo "new_bd 	- создание таблиц при возможности подключения к БД"
	@echo "dbshell - переход в консоль БД"
	@echo "dbtest 	- проверяет существование БД, в случае когда БД не существует выдает сообщение 'database doesn't exist'"
	@echo "flake 	- запуск тестов flake8"
	@echo "venv 	- создание виртуального окружения и установка пакетов из requirements.txt"
	@echo "venv_up - обновление пакетов виртуального окружения"
	@echo "install - полная установка приложения (venv -> new_bd -> test -> flake -> clean)"

# очистка директорий проекта
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .pytest_cache`

# тестирование pytest
test: 
	@if ! [[ -f './.venv/env/bin/pytest' ]]; then\
		$(PIP_DIR) install pytest;\
	fi
	$(ACTIVATE_ENV); PYTHONPATH=. pytest -v
	
# запуск сервера
run: 
	$(FLASK) run

# создание БД и таблиц
new_bd: 
	$(FLASK_DIR) $(COMMAND_BD)

# проверка flake8  
flake: 
	@if ! [[ -f './.venv/env/bin/flake8' ]]; then\
		$(PIP_DIR) install flake8;\
	fi
	$(FLAKE_DIR) --exclude=$(EXCL_PATH) $(ROOT_DIR)

# создание виртуального окружения и установка пакетов
venv:
	mkdir .venv
	cd .venv; virtualenv env
	$(PIP_DIR) install -r requirements.txt 

# обновление пакетов виртуального окружения
venv_up: 
	$(PIP_DIR) install --upgrade pip
	$(PIP_DIR) install --upgrade setuptools
	$(PIP_DIR) install --upgrade wheel
	$(PIP_DIR) freeze > requirements.txt
	$(PIP_DIR) install -r requirements.txt --upgrade

install: venv new_bd test flake clean
	venv
	new_bd
	test
	flake
	clean


dbshell:
	$(FLASK_DIR) dbase dbshell

dbtest:
	$(FLASK_DIR) dbase test
	
	
