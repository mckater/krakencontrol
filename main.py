import server
from data.db_session import global_init


def main():
    global_init("db/population.db")
    server.main()


if __name__ == '__main__':
    main()
