from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy.ext.automap import automap_base

from .config import get_settings


Base = automap_base()
engine = create_engine(get_settings().db_uri, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine)


class JobCard(Base):
    __tablename__ = 'cards'

    description: Mapped['JobDescription'] = relationship(back_populates='card')


class JobDescription(Base):
    __tablename__ = 'descriptions'

    id: Mapped[str] = mapped_column(ForeignKey('cards.id'), primary_key=True)
    card: Mapped['JobCard'] = relationship(back_populates='description')


Base.prepare(autoload_with=engine)
