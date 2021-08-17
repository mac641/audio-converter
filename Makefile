# Docker
docker_dev: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose up --build --remove-orphans dev

docker_prod: .docker/docker-compose.yml .docker/prod.Dockerfile
	docker-compose up --build --remove-orphans prod

# pip requirements
update-requirements: requirements.txt
	pip3 freeze > requirements.txt

install-requirements: requirements.txt
	pip3 install -r requirements.txt

uninstall-requirements:
	pip uninstall -y -r <(pip freeze)

# Babel
scan-translations:
	pybabel extract -F audio_converter/babel.cfg -o audio_converter/translations/messages.pot .

create-translations: audio_converter/translations/messages.pot
	pybabel init -i audio_converter/translations/messages.pot -d audio_converter/translations -l de

update-translations: audio_converter/translations/messages.pot
	pybabel update -i audio_converter/translations/messages.pot -d audio_converter/translations

create-translate: scan-translations create-translations

update-translate: scan-translations update-translations

compile-translations:
	pybabel compile -d audio_converter/translations
