# -*-coding: utf-8-*-

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref

from ..models import (
    DBSession,
    Base
)


class Service(Base):
    __tablename__ = 'service'
    __table_args__ = (
        UniqueConstraint(
            'name',
            name='unique_idx_name_service',
        ),
    )

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True
    )
    resource_id = Column(
        Integer,
        ForeignKey(
            'resource.id',
            name="fk_resource_id_service",
            ondelete='restrict',
            onupdate='cascade',
        ),
        nullable=False,
    )
    resource_type_id = Column(
        Integer,
        ForeignKey(
            'resource_type.id',
            name="fk_resource_type_id_service",
            ondelete='restrict',
            onupdate='cascade',
        ),
        nullable=False,
    )
    name = Column(
        String(length=32),
        nullable=False,
    )
    display_text = Column(
        String(length=255),
        nullable=False,
    )
    descr = Column(
        String(length=255),
    )
    resource = relationship(
        'Resource',
        backref=backref(
            'service',
            uselist=False,
            cascade="all,delete"
        ),
        cascade="all,delete",
        uselist=False,
    )
    resource_type = relationship(
        'ResourceType',
        backref=backref(
            'service',
            uselist=False,
            cascade="all,delete"
        ),
        cascade="all,delete",
        uselist=False,
    )

    @classmethod
    def get(cls, id):
        if id is None:
            return None
        return DBSession.query(cls).get(id)

    @classmethod
    def by_resource_id(cls, resource_id):
        if resource_id is None:
            return None
        return (
            DBSession.query(cls).filter(cls.resource_id == resource_id).first()
        )

    @classmethod
    def by_name(cls, name):
        return DBSession.query(cls).filter(cls.name == name).first()
