from typing import List

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext import automap

from .config import get_settings


Base = automap.automap_base()
engine = create_engine(get_settings().db_uri, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine)


class JobCard(Base):
    __tablename__ = 'cards'

    description: Mapped['JobDescription'] = relationship(back_populates='card')


class JobDescription(Base):
    __tablename__ = 'descriptions'

    @hybrid_method
    def contains_keywords(self, keywords: List[str]):
        return or_(*(self.text.ilike(f"%{keyword}%") for keyword in keywords))


def get_relationship_name(default):
    def wrapper(base, local_cls, referred_cls, constraint) -> str:
        name = default(base, local_cls, referred_cls, constraint)
        return {
            'jobdescription_collection': 'description',
            'jobcard': 'card'
        }.get(name, name)
    return wrapper


Base.prepare(
    autoload_with=engine,
    name_for_scalar_relationship=get_relationship_name(automap.name_for_scalar_relationship),
    name_for_collection_relationship=get_relationship_name(automap.name_for_collection_relationship)
)
