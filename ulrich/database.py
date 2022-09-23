import contextlib
from collections import OrderedDict
import datetime as dt

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext import declarative

import sqlalchemy_utils as sa_utils

import shortuuid

# =============================================================================
# MODELS
# =============================================================================


class ModelABC:
    @orm.declared_attr
    def id(cls):
        return sa.Column(
            sa.Integer,
            sa.Sequence(f"{cls.__tablename__}_id_seq"),
            primary_key=True,
            autoincrement=True,
        )


class UserMixin(ModelABC):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String)


class TagMixin(ModelABC):
    id = sa.Column(sa.Integer, primary_key=True)
    tag = sa.Column(sa.String(255), unique=True, index=True)

    @orm.validates("tag")
    def _convert_upper(self, key, value):
        return value.upper()


class ExperimentMixin(ModelABC):

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(
        sa.String(30), unique=True, default=shortuuid.uuid, index=True
    )
    created_at = sa.Column(sa.DateTime, default=dt.datetime.now)

    @orm.declared_attr
    def owner(cls):
        return sa.orm.relationship("User", backref="experiments", lazy=False)


# =============================================================================
# Connection
# =============================================================================
_MIXINS = list(ModelABC.__subclasses__())


class _Models(OrderedDict):
    """Dict with doted interface."""

    def __getattr__(self, a):
        return self[a]

    def __dir__(self):
        return list(self)


class _DBSession(sa.orm.Session):
    """SQLALchemy session but with a lot of custom operations"""

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db

    @property
    def models(self):
        return self.db.models

    def __repr__(self):
        return f"<{type(self).__name__} '{self.db!r}'>"


class SessionScope(contextlib.AbstractContextManager):
    """Provide a transactional scope around a series of operations."""

    def __init__(self, maker):
        self._maker = maker

    def __enter__(self):
        self._session = self._maker()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()


class Database:
    def __init__(self, dburl):
        self.engine = sa.create_engine(dburl, echo=False)
        self.Base = declarative.declarative_base(name="Base", bind=self.engine)

        self.models = self._create_models(self.Base)
        self.session_maker = orm.sessionmaker(
            class_=_DBSession, bind=self.engine, db=self
        )

    def _create_models(self, Base):
        models = _Models()
        for mixin in _MIXINS:
            attrs = {}

            name = mixin.__name__.removesuffix("Mixin")
            attrs["__tablename__"] = f"ulrich_{name.lower()}"

            models[name] = type(name, (Base, mixin), attrs)

        return models

    # INTERNAL
    def __repr__(self):
        return f"<Database engine={self.engine!r}>"

    # DDL
    def create_database(self):
        return sa_utils.functions.create_database(self.engine.url)

    def create_tables(self):
        return self.Base.metadata.create_all()

    def transaction(self):
        return SessionScope(self.session_maker)
