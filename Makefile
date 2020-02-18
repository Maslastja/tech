ROOT_DIR:= .
PYTHONPATH:= .
VENV_DIR:= $(ROOT_DIR)/.venv/env/bin
PIP:= $(VENV_DIR)/pip
FLASK:= $(VENV_DIR)/flask
FLAKE:= $(VENV_DIR)/flake8
PYTEST:= $(VENV_DIR)/pytest
ACTIVATE_ENV:= . $(VENV_DIR)/activate

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
	@echo "env 	- создание виртуального окружения и установка пакетов из requirements.txt"
	@echo "env_up 	- обновление пакетов виртуального окружения"
	@echo "install - полная установка приложения (env -> new_bd -> test -> flake -> clean)"

# очистка директорий проекта
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .pytest_cache`

# тестирование pytest
test: 
	@if ! [[ -f './.venv/env/bin/pytest' ]]; then\
		$(PIP) install pytest;\
	fi
	$(ACTIVATE_ENV); PYTHONPATH=. pytest -v
	
# запуск сервера
run: 
	$(FLASK) run

# создание БД и таблиц
new_bd: 
	$(FLASK) dbase create-all-tabs

# проверка flake8  
flake: 
	@if ! [[ -f './.venv/env/bin/flake8' ]]; then\
		$(PIP) install flake8;\
	fi
	$(FLAKE) --exclude=$(EXCL_PATH) $(ROOT_DIR)

# создание виртуального окружения и установка пакетов
env:
	mkdir .venv
	cd .venv; virtualenv env
	$(PIP) install -r requirements.txt 

# обновление пакетов виртуального окружения
env_up: 
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
	$(PIP) install --upgrade wheel
	$(PIP) freeze > requirements.txt
	$(PIP) install -r requirements.txt --upgrade

install: env new_bd test flake clean
	env
	new_bd
	test
	flake
	clean


dbshell:
	$(FLASK) dbase dbshell

dbtest:
	$(FLASK) dbase test
	
	
