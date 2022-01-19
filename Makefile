all: build down migrate collectstatic up

pull:
	docker-compose pull

push:
	docker-compose push

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

# $m [migration]
migrate:
	docker-compose run app python manage.py migrate $(if $m,app $m,)

createsuperuser:
	docker-compose run app python manage.py createsuperuser

collectstatic:
	docker-compose run app python manage.py collectstatic --no-input --clear

makemigrations:
	docker-compose run --volume=${PWD}/src:/src app python manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

dev:
	docker-compose run --volume=${PWD}/src:/src --publish=8000:8000 --publish=3000:3000 app python manage.py runserver 0.0.0.0:8000

# $c [service name]
# $p [params string]
logs:
	journalctl CONTAINER_NAME=project_name__$c -o cat $(if $p,$p,)

sh:
	docker exec -it project_name__$c sh

psql:
	docker exec -it project_name__db psql -U postgres

shell:
	docker-compose run app python manage.py shell

# $e [email]
jwt:
	docker-compose run --rm --volume=${PWD}/src:/src app python manage.py shell -c "from app.auth.models import APIUser; print(APIUser.objects.get(email='$e').get_auth_token())"

piplock:
	docker-compose run --rm --no-deps --volume=${PWD}/src:/src --workdir=/src app pipenv install
	sudo chown -R ${USER} src/Pipfile.lock

# $f [filename]
dotenv:
	docker build -t commands ./commands
	docker run commands /bin/sh -c 'python generate_dotenv.py && cat generate_dotenv/.env.example' > $(if $f,$f,.env.tmp)
