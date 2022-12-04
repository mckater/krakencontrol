import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import desc
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=True)
    # SqlAlchemyBase.metadata.drop_all()  #
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)
    session = create_session()
    from data.users import User
    try:
        print(session.query(User).filter(User.name == "SuperAdmin")[0], 'найден, сервис доступен.')
        session.close()
    except IndexError:
        print('Сервис запущен, происходит загрузка первичных данных.')
        session.close()
        start_data_in_bd()  # добавление в БД Супера


def start_data_in_bd():
    session = create_session()
    from data.cities import Citi
    from data.users import User
    from data.krakens import Kraken
    citi_file = open('data/new_cities.csv')
    for nxt_cti in citi_file.readlines():
        citi = Citi()
        data = nxt_cti.split(';')
        citi.citi_name = data[1]
        session.add(citi)
        print(citi)
    citi_file.close()
    user_file = open('data/new_users.csv')
    for nxt_usr in user_file.readlines():
        user = User()
        data = nxt_usr.split(';')
        user.name, user.citi = data[1], int(data[3])
        user.set_password(data[2])
        session.add(user)
        print(user)
    user_file.close()
    kraken_file = open('data/new_krakens.csv')
    for nxt_krkn in kraken_file.readlines():
        kraken = Kraken()
        data = nxt_krkn.split(';')
        kraken.sex, kraken.age, kraken.citi = data[1], int(data[2]), int(data[3])
        kraken.is_childbearing = True if 2 <= kraken.age <= 8 else False
        session.add(kraken)
        print(kraken)
    kraken_file.close()
    session.commit()
    session.close()


def new_kraken_in_bd(kraken):
    session = create_session()
    kraken.is_childbearing = True if 2 <= kraken.age <= 8 else False
    session.add(kraken)
    print(kraken)
    session.commit()
    session.close()


def kraken_del_from_bd(id):
    from data.krakens import Kraken
    session = create_session()
    try:
        kraken = session.query(Kraken).filter_by(id=id).one()
        session.delete(kraken)
        session.commit()
        print('Kraken id {id} is deleted from the database')
    except sa.exc.NoResultFound:  # sqlalchemy.exc.NoResultFound
        print('Kraken id {id} absent in the database')

    # if kraken is not None:
    #     session.delete(kraken)
    #     session.commit()
    #     print('Kraken id {id} is deleted from the database')
    # else:  # sqlalchemy.exc.NoResultFound
    #     print('Kraken id {id} absent in the database')
    session.close()


def query_by_all():
    from data.krakens import Kraken
    session = create_session()
    query = session.query(Kraken).order_by(desc(Kraken.citi), desc(Kraken.is_childbearing))
    li = [str(x).split() for x in query]
    male_count = len([male for male in li if male[-2] == 'True' and male[2] == 'm'])
    female_count = len([female for female in li if female[-2] == 'True' and female[2] == 'f'])
    return [str(x).split() for x in query], (male_count, female_count)


def query_by_citi(what_citi):
    from data.krakens import Kraken
    session = create_session()
    query = session.query(Kraken).filter(Kraken.citi == what_citi).order_by(Kraken.age)
    li = [str(x).split() for x in query]
    male_count = len([male for male in li if male[-2] == 'True' and male[2] == 'm'])
    female_count = len([female for female in li if female[-2] == 'True' and female[2] == 'f'])
    return [str(x).split() for x in query], (male_count, female_count)


def query_citi():
    from data.cities import Citi
    session = create_session()
    query = session.query(Citi).all()
    return {str(c.citi_id): c.citi_name.replace(',', ', ') for c in query}


def query_what_citi(what_citi):
    from data.cities import Citi
    session = create_session()
    query = session.query(Citi).filter(Citi.citi_id == what_citi)[0]
    return query


def create_session() -> Session:
    global __factory
    return __factory()
