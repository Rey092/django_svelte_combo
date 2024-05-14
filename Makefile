# WebServer commands
# ------------------------------
run:
	python manage.py runserver

svelte:
	cd frontend && npm install --force
	cd frontend && npm run dev

init:
	python manage.py migrate
	python manage.py init_project
	python manage.py runserver


# DATABASE
# ------------------------------------------
fix:
	python manage.py reset_db --noinput
	rm -rf ./media/*
	make init

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
	celery -A config.celery_app worker -l info --concurrency=2

beat:
	celery -A config.celery_app beat -l info

# Deployment commands
# ------------------------------
check:
	python manage.py check --configuration=Prod
	python manage.py check --deploy --configuration=Prod

run-dev:
	gunicorn config.wsgi:application

run-prod:
	gunicorn config.wsgi:application
