FROM python:3.10-slim

ENV FLASK_ENV=production
# TODO: figure out how to send emails for registration etc. without using a private web.de account

WORKDIR /app

# Install requirements
RUN /usr/local/bin/python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg apt-utils
RUN /bin/rm -f requirements.txt

RUN python3 -m pip install gunicorn

ADD . /app

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi"]

COPY .docker/prod-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/prod-entrypoint.sh
ENTRYPOINT ["prod-entrypoint.sh"]
