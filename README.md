# Project Name

This is a template project for future Django projects. It is designed to be a starting point for any new Django project, providing a solid foundation of best practices and sensible defaults.

## Requirements

- Python 3.12
- Django
- PostgreSQL

## Libraries Used

- Django
- django-configurations
- django-allauth
- django_celery_beat
- django_redis
- django_cleanup
- django_extensions

## Getting Started

To initialize the project, follow these steps:

1. Clone the repository: `git clone https://github.com/username/project.git`
2. Navigate to the project directory: `cd project`
3. Install the requirements: `pip install -r requirements.txt`
4. Initialize the project: `make init`
5. Run the server: `make run`

## Commands

- `make run`: Run the server
- `make init`: Initialize the project
- `make fix`: Reset the database and initialize the project
- `make migrations`: Make migrations
- `make migrate`: Apply migrations
- `make messages`: Make translation messages
- `make compile`: Compile translation messages
- `make worker`: Run Celery worker
- `make beat`: Run Celery beat
- `make check`: Check the project
- `make run-dev`: Run the server in development mode
- `make run-prod`: Run the server in production mode

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
