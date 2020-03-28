#!/usr/bin/env python
import json
import os
import time

from confluent_kafka import Producer
from flask import Flask, jsonify

from src.config import Config
from src.custom_exeptions import RunnerMetadataExrtactionException, \
    RunnerFormatException
from src.dao import db
from src.services.runner import RunnerService
from src.utils.files import is_runner_safe, get_runner_metadata, \
    save_file_in_tmp_folder
from src.utils.logger import get_logger
from src.utils.requests import parse_request
from src.utils.responses import Error404Response, Ok20XResponse

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
    commit_hash = data['commit_hash']
    commiter = data['commiter']
    # Get one and only one runner script
    uploaded_file = data['files'].get('runner')
    tmp_save_path = save_file_in_tmp_folder(
        uploaded_file, config.TEMP_UPLOAD_FOLDER)
    # Check runner on maliciousness
    is_safe, results = is_runner_safe(tmp_save_path)
    os.remove(tmp_save_path)
    if not is_safe:
        return jsonify(Error404Response({'reason': results}).to_dict())
    try:
        metadata = get_runner_metadata(uploaded_file)
        if not metadata:
            return jsonify(Error404Response(
                {'reason': 'Error empty metadata, please check your runner'}
            ).to_dict())
    except (RunnerMetadataExrtactionException, RunnerFormatException):
        return jsonify(Error404Response(
            {'reason': 'Error while calling metadata on runner'}).to_dict())
    context = {
        'commit_hash': commit_hash,
        'uploaded_file': uploaded_file,
        'commiter': commiter,
        'name': metadata.get('name'),
        'description': metadata.get('description'),
        'department': metadata.get('department')
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
    return jsonify(Ok20XResponse(update).to_dict())
    return "Ok"


app.run('0.0.0.0', config.SERVICE_PORT, debug=config.SERVICE_DEBUG)
