import json
import os
import subprocess as sp
import time

from src.custom_exeptions import RunnerFormatException, \
    RunnerMetadataExrtactionException


def is_runner_safe(tmp_path):
    process = sp.Popen(['bandit', '-r', '-f', 'json', tmp_path],
                               stdout=sp.PIPE)
    stdout = process.communicate()[0]
    report = json.loads(stdout)
    results = report.get('results', [])
    return len(results) == 0, results


def get_runner_metadata(uploaded_file):
    uploaded_file.seek(0)
    file_str = uploaded_file.read()
    uploaded_file.seek(0)
    _locals = {'klass': None,}
    exec(file_str, {'__builtins__': __builtins__}, _locals)
    klass = _locals.get('klass')
    # TODO: set this on compute
    # exec(file_str, {'__builtins__': __builtins__, 'np': np}, _locals)
    # gen = klass(func).execute()
    # for res, per in gen:
    #     print(res, '----', per)
    if not klass:
        raise RunnerFormatException()
    if is_method_in_class(klass, 'execute') and \
            is_method_in_class(klass, 'metadata'):
        try:
            return klass.metadata()
        except Exception as e:
            raise RunnerMetadataExrtactionException()


def save_file_in_tmp_folder(uploaded_file, config_tmp_path):
    tmp_file_name = str(time.time())
    tmp_save_path = os.path.join(config_tmp_path, tmp_file_name)
    uploaded_file.save(tmp_save_path)
    return tmp_save_path


def is_method_in_class(klass, method):
    return method in dir(klass)
