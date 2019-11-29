FROM python:2.7-slim

#Commands to deal with HORRIFIC FIREWALL ISSUES
#ENV http_proxy "http://yourinfo"
#ENV https_proxy "http://yourinfo"
#ENV no_proxy "localhost"

RUN python -m pip --no-cache-dir install numpy psycopg2-binary gunicorn celery==4.2.2
RUN python -m pip --no-cache-dir install --upgrade https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2

# OpenREM installation
COPY ./app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
#WORKDIR /app/openrem #Comment line to force refresh
#COPY ./app /app
WORKDIR /app/openrem

RUN echo '127.0.0.1 localhost\n127.0.1.1 openremserver' >> /etc/hosts && \
adduser $USER openrem && \
mkdir /var/dose && \
cd /var/dose && \
mkdir pixelmed && \
mkdir static

#ADD ./pixelmed.jar /var/dose/pixelmed/pixelmed.jar
COPY ./initialise.sh /var/dose/initialise.sh

#RUN sed -i 's/localhost:15672/rabbitmq:15672/g' /app/remapp/views.py

CMD bash
