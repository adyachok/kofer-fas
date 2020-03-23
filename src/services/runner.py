import os
from datetime import datetime

from werkzeug.utils import secure_filename

from src.dao.sql_models import Runner, RunnerFile
from src.repositories.sql_repository import SqlRepository


class RunnerService:

    def __init__(self, app):
        self.application = app
        self.config = self.application.config['env_config']
        self.sql_repo = SqlRepository(self.application)

    def process_runner_file(self, uploaded_file, commiter, commit_hash,
                            revision):
        runner_file = self.process_received_runner_file(
            self.config.UPLOAD_FOLDER,
            uploaded_file,
            commiter,
            commit_hash)
        runner_file.revision = revision
        return runner_file

    def create_runner(self, name, description, department, commiter,
                      commit_hash, uploaded_file):
        created = False
        runner = self.sql_repo.get_runner_by_name_and_dept(name, department)
        if not runner:
            runner = Runner(name, description, department)
            created = True
        else:
            self.update_runner_revision(runner)
        runner_file = self.process_runner_file(
                uploaded_file, commiter, commit_hash, runner.current_revision)
        runner.files.append(runner_file)
        self.sql_repo.create_or_update_runner(runner)
        return runner, created

    def update_runner_revision(self, runner):
        revision = runner.current_revision
        if runner.files and len(runner.files):
            revision = max([runner_file.revision for runner_file in
                            runner.files])
        runner.current_revision = revision + 1

    def process_received_runner_file(self, base_upload_folder, received_file,
                                     commiter, commit_hash):
        """Process runner file
        :param base_upload_folder:
        :param received_file:
        :return:
        """
        folder_name = datetime.utcnow().strftime('%Y-%m-%d_%H_%M_%S_%f')
        upload_dir_path = os.path.join(base_upload_folder, folder_name)
        if not os.path.exists(upload_dir_path):
            os.makedirs(upload_dir_path)
        if received_file.filename == '':
            raise Exception('Error: no file name')
        filename = secure_filename(os.path.basename(received_file.filename))
        runner_file = RunnerFile(commiter, commit_hash)
        save_path = os.path.join(upload_dir_path, filename)
        received_file.save(save_path)
        runner_file.file_path = save_path
        return runner_file
