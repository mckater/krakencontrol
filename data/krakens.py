import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class Kraken(SqlAlchemyBase):
    __tablename__ = 'krakens'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date_in_bd_added = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_childbearing = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)  # в детородном возрасте
    citi = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cities.citi_id"))

    def __repr__(self):
        return f'<Kraken> {self.id} {self.sex} {self.age} {self.is_childbearing} {self.citi}'
