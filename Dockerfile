FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y python3-pip \
    && apt-get install nano \
    && apt-get install default-jdk wget -y

RUN pip3 install -U tox wheel six setuptools
# RUN pip3 install dbt-postgres

RUN wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
RUN tar -xvzf spark-3.2.0-bin-hadoop3.2.tgz
RUN mv spark-3.2.0-bin-hadoop3.2 /opt/spark
RUN export SPARK_HOME=/opt/spark
RUN export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN mkdir /usr/app

WORKDIR /usr/app
VOLUME /usr/app

ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8

COPY . /usr/app/.
RUN pip3 install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]