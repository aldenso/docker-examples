FROM python:alpine3.6

RUN apk update && apk add mariadb-client-libs

ADD . /src
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "/src/run.py"]
