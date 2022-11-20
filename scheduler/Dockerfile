FROM python:3.9

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install -y sudo less python3-dev build-essential

RUN apt-get autoremove -y

ADD . /app/

RUN pip3 install -r ./requirements/main.txt

ENTRYPOINT ["python3", "main.py"]
