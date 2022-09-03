# Local commands
# Docker
run_docker_dev: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose -f .docker/docker-compose.yml build --no-cache --force-rm dev; \
docker-compose -f .docker/docker-compose.yml up -d --remove-orphans dev

run_docker_prod: .docker/docker-compose.yml .docker/prod.Dockerfile
	docker-compose -f .docker/docker-compose.yml build --no-cache --force-rm prod; \
docker-compose -f .docker/docker-compose.yml up -d --remove-orphans prod

.PHONY: stop_docker_dev
stop_docker_dev: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose -f .docker/docker-compose.yml kill dev

.PHONY: stop_docker_prod
stop_docker_prod: .docker/docker-compose.yml .docker/dev.Dockerfile
	docker-compose -f .docker/docker-compose.yml kill prod

# Misc
.PHONY: clean
clean: clean-logs clean-converting-directories clean-db

.PHONY: clean-logs
clean-logs:
	/bin/rm -f **/**.log

.PHONY: clean-converting-directories
clean-converting-directories:
	cd media; /bin/rm -rf uploads converted downloadable; cd ..

clean-db: media/database.sqlite
	/bin/rm -f media/database.sqlite

user_config: .scripts/create_user_config.sh
	sh .scripts/create_user_config.sh

# Virtualized commands
# pip requirements
update-requirements: requirements.txt
	pip3 freeze > requirements.txt

install-requirements: requirements.txt
	pip3 install -r requirements.txt

uninstall-requirements:
	pip3 uninstall -y -r <(pip3 freeze)

update-packages:
	pip3 list -o | grep -v -i warning | cut -f1 -d' ' | tr " " "\n" | awk '{if(NR>=3)print}' | cut -d' ' -f1 \
| xargs -n1 pip3 install -U

# Babel
.PHONY: scan-translations
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
