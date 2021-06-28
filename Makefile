update-requirements: requirements.txt
	pip3 freeze > requirements.txt

scan-translation:
	pybabel extract -F babel.cfg -o translate.pot audio-converter/

create-translation: translate.pot
	pybabel init -i translate.pot -d audio-converter/translations -l de

compile-translations:
	pybabel compile -d audio-converter/translations

translate: scan-translation create-translation compile-translations

docker_dev: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose up --build --remove-orphans dev

docker_prod: .docker/docker-compose.yml .docker/prod.Dockerfile
	docker-compose up --build --remove-orphans prod
