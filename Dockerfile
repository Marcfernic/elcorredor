FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3.8


From python:3.9.16-alpine3.16

Env PYTHONUNBUFFERED=1

Workdir /app

Copy requirements.txt requirements.txt

RUN pip install -r requirements.txt

Copy ./ ./

ENTRYPOINT ["python3"]

Cmd ["manage.py","runserver","0.0.0.0:8000"]