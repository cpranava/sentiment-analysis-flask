FROM centos:7

USER root

RUN yum install python3 wget python3-devel -y

COPY . /app

WORKDIR /app/

EXPOSE 5000

RUN pip3 install -r /app/requirements.txt

RUN python3 -c 'import nltk; nltk.download("vader_lexicon")'

CMD python3 /app/app.py
