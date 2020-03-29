import json
from datetime import datetime

from sqlalchemy import and_

from src.dao import db
from src.utils.logger import get_logger


logger = get_logger('sql_models')


def to_camel_case(dict_obj):
    json_dict = {}
    for key, val in dict_obj.items():
        if '_' in key and not key.startswith('_'):
            for i, c in enumerate(key):
                if c == '_':
                    key = key[:i] + key[i+1:].capitalize()
            key = key.replace('_', '')
        if isinstance(val, dict):
            json_dict[key] = to_camel_case(val)
        else:
            json_dict[key] = val
    return json_dict


class BaseMixin(object):
    """Used as composition part in entities which need create, update
    functionality."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def serialize(self):
        raise NotImplementedError

    def toJson(self):
        dict_obj = self.serialize()
        json_dict = to_camel_case(dict_obj)
        return json.dumps(json_dict)


class Runner(BaseMixin, db.Model):
    __tablename__ = 'runner'
    id = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    department = db.Column(db.String(50), primary_key=True, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    current_revision = db.Column(db.Integer, nullable=False, default=1)
    files = db.relationship('RunnerFile', backref='runner', lazy=True)

    __mapper_args__ = {
        'primary_key': [name, department]
    }
    __table_args__ = (db.UniqueConstraint('name', 'department'), {})

    def __init__(self, name, description, department):
        self.name = name
        self.description = description
        self.department = department

    def __repr__(self):
        return '<Runner name: %r dept: %r revision: %r>' % (
            self.name, self.department, self.current_revision)

    def serialize(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'department': self.department,
            'current_revision': self.current_revision,
            'file': self._get_current_runner_file(),
            'createdAt': self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            'updatedAt': self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }
        return data

    def _get_current_runner_file(self):
        revision = self.current_revision
        runner_file = RunnerFile.query \
            .filter(and_(RunnerFile.runner_name == self.name,
                         RunnerFile.runner_department == self.department,
                         RunnerFile.revision == self.current_revision))  \
            .first()
        if not runner_file:
            msg = f'''Any runner file object with runner id
                    {self.id} and revision number {revision} was found'''
            logger.error(msg)
            return
        return runner_file.serialize()


class RunnerFile(BaseMixin, db.Model):
    """Describes runner file."""
    __tablename__ = 'runner_file'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(250), nullable=False)
    runner_name = db.Column(db.String(50), nullable=False)
    runner_department = db.Column(db.String(50), nullable=False)
    commiter = db.Column(db.String(120), nullable=False)
    commit_hash = db.Column(db.String(80), nullable=False)
    revision = db.Column(db.Integer, nullable=False, default=1)
    # runner = db.relationship("Runner", back_populates="files")

    __table_args__ = (
        db.ForeignKeyConstraint(['runner_name', 'runner_department'],
                                ['runner.name', 'runner.department']),)

    def __init__(self, commiter, commit_hash):
        self.commiter = commiter
        self.commit_hash = commit_hash

    def __repr__(self):
        return '<RunnerFile path: %r commiter: %r commit_hash: %r>' % (
            self.file_path, self.commiter, self.commit_hash)

    def serialize(self):
        return {
            'filePath': self.file_path,
            'commiter': self.commiter,
            'revision': self.revision,
            'commit_hash': self.commit_hash,
            'createdAt': self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            'updatedAt': self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        }
