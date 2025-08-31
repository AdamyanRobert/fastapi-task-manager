from src.database import sync_engine
from src.database import Base
from src.models.tasks import Base as TaskBase


def create_all_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


create_all_tables()
