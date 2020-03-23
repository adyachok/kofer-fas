#!/usr/bin/env python
import json
import os

from confluent_kafka import Producer
from flask import Flask, jsonify

from src.config import Config
from src.dao import db
from src.services.runner import RunnerService
from src.utils.logger import get_logger
from src.utils.requests import parse_request


logger = get_logger('app')
app = Flask(__name__)
config = Config(app, db)
app.config['env_config'] = config
p = Producer({'bootstrap.servers': config.BOOTSTRAP_SERVERS,
              'group.id': 'fas'})


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')


@app.route('/', methods=["POST"])
def upload():
    """Processes data-science script, check on malicious logic.
    Expects POST request with next fields:
       - commit hash (str)
       - commit pusher (str)
       - runner (byte)
    Runner should have next method:
        metadata() -> str
    :return:
    """
    data = parse_request()
    name = data['name']
    description = data['description']
    department = data['department']
    commit_hash = data['commit_hash']
    commiter = data['commiter']
    # get one and only one runner script
    uploaded_file = data['files'].get('runner')
    # TODO: check runner on maliciousness
    # TODO: get runner metadata
    context = {
        'commit_hash': commit_hash,
        'uploaded_file': uploaded_file,
        'commiter': commiter,
        'name': name,
        'description': description,
        'department': department
    }
    runner, created = RunnerService(app).create_runner(**context)
    update = {}
    if runner:
        update = runner.serialize()
        file_path = update['file'].pop('filePath')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                update['file']['code'] = f.read()
        else:
            update['file']['code'] = ""
        p.produce('runner-update',
                  json.dumps(update),
                  callback=delivery_report)
        p.flush()
        logger.info(runner)
    return jsonify(update)


app.run('0.0.0.0', config.SERVICE_PORT, debug=config.SERVICE_DEBUG)
