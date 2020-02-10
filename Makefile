ROOT_DIR= .
VENV_DIR:= $(ROOT_DIR)/.venv/env
ACTIVATE_ENV= . $(VENV_DIR)/bin/activate
PYTHONPATH= . pytest
COMMAND_BD= flask dbase create-all-tabs
EXCL_PATH= .git,.venv,static,logs,.gitignore,__pycache__

# очистка директорий проекта
clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .pytest_cache`

# тестирование pytest
test:
	$(ACTIVATE_ENV); pytest -v $(ROOT_DIR)
	
# запуск сервера
serv:
	$(ACTIVATE_ENV); flask run

# создание БД и таблиц
new_bd:
	$(ACTIVATE_ENV); $(COMMAND_BD)

# проверка flake8  
flake:
	flake8 --exclude=$(EXCL_PATH) $(ROOT_DIR)

# создание виртуального окружения и установка пакетов
	venv:
	mkdir .venv
	cd .venv; virtualenv env
	$(ACTIVATE_ENV); pip install -r requirements.txt 

# обновление пакетов виртуального окружения
venv_up:
	$(ACTIVATE_ENV); pip freeze > requirements.txt; pip install -r requirements.txt --upgrade
