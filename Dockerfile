FROM python:3.8-alpine
WORKDIR /home
RUN mkdir -p stiqueue
ADD stiqueue stiqueue/stiqueue
ADD example stiqueue/example
ADD tests stiqueue/tests
ADD scripts stiqueue/scripts
COPY *.sh stiqueue
COPY requirements.txt stiqueue/
RUN cd stiqueue; python -m venv .venv ; .venv/bin/pip install -r requirements.txt ; .venv/bin/python -W ignore  -m unittest tests/*
#ENTRYPOINT sh
ENTRYPOINT cd stiqueue ; .venv/bin/python -m stiqueue.sqserver