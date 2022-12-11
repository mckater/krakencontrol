import sqlalchemy

from data.db_session import SqlAlchemyBase


class Citi(SqlAlchemyBase):
    __tablename__ = 'cities'

    citi_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    citi_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f'{self.citi_name}'
