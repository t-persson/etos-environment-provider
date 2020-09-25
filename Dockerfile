FROM python:3.8.3

ARG PIP_ARGS

RUN useradd -ms /bin/bash etos
USER etos

ENV PATH="/home/etos/.local/bin:${PATH}"

RUN pip install $PIP_ARGS --upgrade pip

WORKDIR /var/www/html/src
CMD ["./entry.sh"]

COPY requirements.txt /requirements.txt
RUN pip install $PIP_ARGS -r /requirements.txt
COPY . /var/www/html
