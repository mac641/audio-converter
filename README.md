![docker hub deployment](https://github.com/mac641/audio-converter/actions/workflows/deploy.yml/badge.svg)

<div align="center">
  <img width="300px" src="./audio_converter/static/img/Logo.png" alt="audio-converter logo">
</div>

audio-converter allows you to convert audio files from within your web browser.

## Production Usage

1. Create a new directory which will hold all interactive files (e.g. the database, logs, converted files) by typing
   `mkdir -p media` in a terminal. This directory has to be created in this project's root directory.
2. Create a user config file by typing `make user_config` in your terminal.
   1. Open the new file (media/user_config.py) and fill up the example placeholder between the quotation marks.
   2. Save the file.
3. Adjust the timezone to your needs by editing `TZ` under `environment:` in `.docker/docker-compose.yml`.
4. Start the server!
   - If you want to build and start the production server locally, type `make run_docker_prod` in your
     terminal.
   - Alternatively you can pull a pre-built image
     from [DockerHub](https://hub.docker.com/r/mac641/audio-converter). Follow the instructions on DockerHub
     to run the server.

## How to contribute

1. Make sure you have `docker`/`podman` and `docker-compose` installed.
2. If using PyCharm, add a new _Docker-Compose_ Interpreter
   ([Jetbrains Guide: Configuring Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#tw))
   to enable linting.
3. Create a user config file by typing `make user_config` in your terminal.
   1. Open the new file (media/user_config.py) and fill up the example placeholder between the quotes.
   2. Save the file.
