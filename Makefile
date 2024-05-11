# WebServer commands
# ------------------------------
run:
	python manage.py runserver

# DATABASE
# ------------------------------------------
fix:
	python manage.py reset_db --noinput
	python manage.py migrate
	rm -rf ./media/*
	python manage.py currencies -i ALBA_CURRENCIES
	python manage.py init_project
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

# TRANSLATIONS
# ------------------------------------------
messages:
	python manage.py makemessages -l uk -s

compile:
	python manage.py compilemessages -l uk


# CELERY
# ------------------------------------------
worker:
	celery -A config.celery worker -l info --concurrency=2

beat:
	celery -A config.celery beat -l info

# Deployment commands
# ------------------------------
check:
	python manage.py check --configuration=Prod
	python manage.py check --deploy --configuration=Prod

run-dev:
	# TODO: Add dev
	python manage.py runserver

run-prod:
	# TODO: Add prod
	python manage.py runserver
