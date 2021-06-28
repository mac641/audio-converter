update-requirements: requirements.txt
	pip3 freeze > requirements.txt

scan-translation:
	pybabel extract -F audio_converter/babel.cfg -o audio_converter/translations/messages.pot audio_converter/

create-translation: audio_converter/translations/messages.pot
	pybabel init -i audio_converter/translations/messages.pot -d audio_converter/translations -l de

compile-translations:
	pybabel compile -d audio_converter/translations

translate: scan-translation create-translation compile-translations

docker_dev: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose up --build --remove-orphans dev

docker_prod: .docker/docker-compose.yml .docker/prod.Dockerfile
	docker-compose up --build --remove-orphans prod
