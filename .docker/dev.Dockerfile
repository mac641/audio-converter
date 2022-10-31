FROM python:3.11.0-slim

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST='0.0.0.0'
ENV FLASK_ENV=developement
ENV FLASK_DEBUG=1

WORKDIR /app

RUN /usr/local/bin/python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg make apt-utils
RUN /bin/rm -f requirements.txt

CMD ["python3", "-m", "flask", "run"]

COPY .docker/dev-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/dev-entrypoint.sh
ENTRYPOINT ["dev-entrypoint.sh"]
