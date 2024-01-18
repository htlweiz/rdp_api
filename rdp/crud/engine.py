from sqlalchemy import create_engine as sql_create_engine


def create_engine(url):
    return sql_create_engine(url, echo=True)