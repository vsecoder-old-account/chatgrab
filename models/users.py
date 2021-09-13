import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True)
    name = sa.Column(sa.String, nullable=True)
    fullname = sa.Column(sa.String, nullable=True)
    username = sa.Column(sa.String, nullable=True)
    data = sa.Column(sa.String, nullable=True)
    work = sa.Column(sa.String, nullable=True)
