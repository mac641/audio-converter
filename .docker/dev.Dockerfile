FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "-m" , "flask", "run"]