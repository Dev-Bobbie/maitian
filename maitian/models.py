from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,Float
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from maitian.settings import MYSQL_PIPELINE_URL

engine = create_engine(f"mysql+py{MYSQL_PIPELINE_URL}?charset=utf8", max_overflow=5)

Base = declarative_base()

class Article(Base):

    """
    title = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    district = scrapy.Field()
    """
    __tablename__ = 'zufang'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    area = Column(String(300), nullable=False)
    district = Column(String(50),nullable=False)


    __table_args__ = (
        {"mysql_engine": "InnoDB","mysql_charset": "utf8"}, # 表的引擎
    )


def is_database_exists():
    if not database_exists(engine.url):
        create_database(engine.url)
        return False
    return True

def create_all_table():
    # 创建所有表
    Base.metadata.create_all(engine)

def drop_all_table():
    # 删除所有表
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    if not is_database_exists():
        create_all_table()
    # drop_all_table()