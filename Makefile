# WebServer commands
# ------------------------------
run:
	python manage.py runserver

svelte:
	nvm use --lts
	npm install --force
	npm run dev

init:
	python manage.py migrate
	python manage.py init_project
	npm install --force
	python manage.py runserver

shell:
	python manage.py shell_plus


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
	#python manage.py runserver --configuration=Prod
	#gunicorn -c gunicorn_conf.py config.wsgi:application
	python manage.py migrate
	#python manage.py fix_manifest
	python manage.py collectstatic --no-input
	gunicorn -c gunicorn_conf.py config.wsgi:application
