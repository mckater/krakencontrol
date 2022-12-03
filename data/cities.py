# import datetime
import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Citi(SqlAlchemyBase):
    __tablename__ = 'cities'

    citi_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    citi_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    # is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    # citi_admin_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    # user = orm.relation('User')

    def __repr__(self):
        return f'{self.citi_name}'