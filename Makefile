# Docker
docker_dev: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose -f .docker/docker-compose.yml build --no-cache --force-rm dev; \
docker-compose -f .docker/docker-compose.yml up -d --remove-orphans dev

docker_prod: .docker/docker-compose.yml .docker/prod.Dockerfile
	docker-compose -f .docker/docker-compose.yml build --no-cache --force-rm prod; \
docker-compose -f .docker/docker-compose.yml up -d --remove-orphans prod

# pip requirements
update-requirements: requirements.txt
	pip3 freeze > requirements.txt

install-requirements: requirements.txt
	pip3 install -r requirements.txt

uninstall-requirements:
	pip uninstall -y -r <(pip freeze)

update-packages:
	pip3 list -o | grep -v -i warning | cut -f1 -d' ' | tr " " "\n" | awk '{if(NR>=3)print}' | cut -d' ' -f1 |
	xargs -n1 pip3 install -U

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
