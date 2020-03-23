from sqlalchemy import and_

from src.dao.sql_models import Runner


class SqlRepository:

    def __init__(self, app):
        self.application = app
        self.config = self.application.config['env_config']

    def save_object(self, obj):
        """Saves entities to the database"""
        with self.application.app_context():
            self.config.db.session.add(obj)
            self.config.db.session.commit()

    def create_or_update_runner(self, runner):
        with self.application.app_context():
            if runner.id:
                self.config.db.session.merge(runner)
            else:
                self.config.db.session.add(runner)
            self.config.db.session.commit()
            return runner.id, None

    def get_runner_by_name_and_dept(self, name, department):
        return Runner.query.filter(and_(Runner.name == name,
                                        Runner.department == department)) \
            .first()
