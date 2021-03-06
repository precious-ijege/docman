FROM python:2.7-jessie

MAINTAINER precious.ijege@andela.com

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt

ONBUILD COPY . /usr/src/app

CMD ["bash", "/usr/src/app/script.sh"]