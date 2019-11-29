from celery import Celery
import os
import dicom
from process_file import process_file

app = Celery('openrem_process', backend='rpc://', broker='amqp://guest:guest@rabbitmq//')
app.conf.task_default_queue = 'test'

BASEDIR="/var/img"

@app.task
def process(filename):
    print(filename)
    process_file(filename)

