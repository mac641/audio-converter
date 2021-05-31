FROM python:3.9-alpine

WORKDIR ./app
RUN python3 -m venv audio_converter
RUN apk add bash
RUN /bin/bash -c "source audio_converter/bin/activate"
COPY ./requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]