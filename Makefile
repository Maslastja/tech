ROOT_DIR:= .
PYTHONPATH:= .
VENV_DIR:= $(ROOT_DIR)/.venv/bin
PIP:= $(VENV_DIR)/pip
FLASK:= $(VENV_DIR)/flask
FLAKE:= $(VENV_DIR)/flake8
PYTEST:= $(VENV_DIR)/pytest
ACTIVATE_ENV:= . $(VENV_DIR)/activate

# директории и файлы, которые необходимо исключить при проверке кода flake8
EXCL_PATH= .git,.venv,static,logs,.gitignore,__pycache__

help:
	@echo "clean 	   - удаление кеша"
	@echo "test 	   - запуск тестов pytest"
	@echo "run 	   - запуск сервера"
	@echo "create_db   - создание таблиц при возможности подключения к БД"
	@echo "shell_db    - переход в консоль БД"
	@echo "flake 	   - запуск тестов flake8"
	@echo "env 	   - создание виртуального окружения и установка пакетов из requirements.txt"
	@echo "env_up 	   - обновление пакетов виртуального окружения"
	@echo "env_list	   - выводит на экран список установленных пакетов в виртуальное окружение"
	@echo "env_install - устанавливает/обновляет пакеты в виртуальное окружение"
	@echo "install 	   - полная установка приложения (env -> create_db)"

# очистка директорий проекта
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .pytest_cache`

# тестирование pytest
test: 
	@if ! [[ -f './.venv/bin/pytest' ]]; then\
		$(PIP) install pytest;\
	fi
	$(ACTIVATE_ENV); PYTHONPATH=. pytest -v; deactivate
	
# запуск сервера
run: 
	$(FLASK) run

# создание БД и таблиц
create_db: 
	$(FLASK) db create-all-tabs

# проверка flake8  
flake: 
	@if ! [[ -f './.venv/bin/flake8' ]]; then\
		$(PIP) install flake8;\
	fi
	$(FLAKE) --exclude=$(EXCL_PATH) $(ROOT_DIR)

# создание виртуального окружения и установка пакетов
env: 
	python3 -m venv .venv
	$(PIP) install -r requirements.txt 

# обновление пакетов виртуального окружения
env_up: 
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
	$(PIP) install --upgrade wheel

# вывод списка установленных пакетов
env_list:
	$(PIP) list

# установка/обновление пакетов
env_install:
	@if [ "${PACK_NAME}" ]; then\
		$(PIP) install $(PACK_NAME) --upgrade;\
	else\
		echo 'необходимо указать название пакета: make pip_install PACK_NAME=*name*';\
	fi
	
# полная установка приложения (виртаульное окружение, база данных)
install: env create_db

# запуск консоли базы данных
shell_db:
	$(FLASK) db shell-db

	
	
