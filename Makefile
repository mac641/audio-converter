build_dev: .docker/docker-compose.yml dev.Dockerfile
	docker-compose up --build --remove-orphans dev

build_prod: .docker/docker-compose.yml prod.Dockerfile
	docker-compose up --build --remove-orphans prod

update-requirements: requirements.txt
	pip3 freeze > requirements.txt

install-requirements: requirements.txt
	pip3 install -r requirements.txt

uninstall-requirements:
	pip uninstall -y -r <(pip freeze)
