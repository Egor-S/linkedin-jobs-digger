import datetime
from typing import Optional

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class JobCard(Base):
    __tablename__ = 'cards'

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    company: Mapped[str]
    location: Mapped[str]
    date: Mapped[datetime.date]
    first_seen: Mapped[datetime.datetime] = mapped_column(default_factory=datetime.datetime.utcnow, init=False)
    last_seen: Mapped[datetime.datetime] = mapped_column(default_factory=datetime.datetime.utcnow, init=False)
    description: Mapped['JobDescription'] = relationship(back_populates='card', init=False, default=None)


class JobDescription(Base):
    __tablename__ = 'descriptions'

    id: Mapped[str] = mapped_column(ForeignKey('cards.id'), init=False, primary_key=True)
    type: Mapped[str]
    text: Mapped[str]
    lang: Mapped[str] = mapped_column(String(2))
    seniority: Mapped[Optional[str]] = mapped_column(default=None)
    function: Mapped[Optional[str]] = mapped_column(default=None)
    industries: Mapped[Optional[str]] = mapped_column(default=None)
    card: Mapped['JobCard'] = relationship(back_populates='description', init=False, default=None)
