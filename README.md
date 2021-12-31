# audio-converter

This repo contains a Python project which allows you to convert audio files from within your web browser.

## Production Usage

1. Create a User config file by typing `make user_config` in your terminal.
    1. Open the new file (user_config.py) and fill up the example placeholder between the quotation marks.
    2. Save the file.
2. Start the production server by typing `make docker_prod` in your terminal.

## How to contribute

1. Make sure you have `docker`/`podman` and `docker-compose` installed.
2. If using PyCharm, add a new *Docker-Compose* Interpreter
   ([Jetbrains Guide: Configuring Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#tw))
   to enable linting.
3. Create a User config file by typing `make user_config` in your terminal.
    1. Open the new file (user_config.py) and fill up the example placeholder between the quotation marks.
    2. Save the file.
4. For testing your code, you can either start `audio-converter_dev` by typing `make docker_dev` in your terminal or add
   a configuration to your PyCharm.

## Zoom Meeting

[Click here](https://hs-augsburg.zoom.us/j/94338900433?pwd=a2NhUDJMRk1OeTYwMnZpQ3lJbXo1UT09)

## HackMD - Report

[Click here](https://hackmd.io/ymKcuO0yQ0azINDnV-Y3rw?both#)
