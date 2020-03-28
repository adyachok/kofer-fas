import os

from src.utils.logger import get_logger


logger = get_logger('config')


class Config:

    UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'uploads')
    TEMP_UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'tmp_uploads')
    # max runner file size 50 Kb
    MAX_CONTENT_LENGTH = 50 * 1024
    SERVICE_PORT = 5000
    SERVICE_DEBUG = True
    BOOTSTRAP_SERVERS = 'localhost:9092'

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self._init_kafka_bootstrap_servers()
        self._init_service_port()
        self._init_db(app)
        self._clear_tables(app)

    def _init_db(self, app):
        postgresql_database = os.getenv('POSTGRESQL_DATABASE')
        if not postgresql_database:
            postgresql_database = 'zz_fas'

        postgresql_password = os.getenv('POSTGRESQL_PASSWORD')
        if not postgresql_password:
            postgresql_password = 'testp'

        postgresql_username = os.getenv('POSTGRESQL_USERNAME')
        if not postgresql_username:
            postgresql_username = 'testu'

        postgresql_host = os.getenv('POSTGRESQL_HOST')
        if not postgresql_host:
            postgresql_host = 'localhost'

        logger.info('Connection properties: DB: %s, User: %s, Host: %s' % (
            postgresql_database, postgresql_username, postgresql_host))
        # Flask-SQLAlchemy should extract connection string from the
        # application config
        app.config['SQLALCHEMY_DATABASE_URI'] = build_connection_url(
            postgresql_username,
            postgresql_password,
            postgresql_host,
            5432,
            postgresql_database)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db.init_app(app)

    def _init_kafka_bootstrap_servers(self):
        bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')
        if bootstrap_servers:
            self.BOOTSTRAP_SERVERS = bootstrap_servers

    def _init_service_port(self):
        port = os.getenv('SERVICE_PORT')
        if port:
            self.SERVICE_PORT = port

    def _clear_tables(self, app):
        if os.getenv('INIT_DATABASE_ON_START'):
            self.db.drop_all(app=app)
            self.db.create_all(app=app)


def build_connection_url(user, password, host, port, dbname):
    return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
