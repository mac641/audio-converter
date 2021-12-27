FROM python:3.10-slim

ENV FLASK_ENV=production
# TODO: figure out how to send emails for registration etc. without using Lukas's web.de account :D

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN /bin/rm -f requirements.txt

RUN python3 -m pip install gunicorn

ADD . /app

# TODO: persist database (maybe use volumes)
RUN if [ ! -f database.sqlite ]; then \
      python3 create_db.py; \
    fi

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi"]
