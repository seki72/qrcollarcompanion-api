from datetime import datetime, timedelta, timezone
from uuid import uuid4

import flask_sqlalchemy
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_mixins import AllFeaturesMixin

db = flask_sqlalchemy.SQLAlchemy()


class BaseModel(db.Model, AllFeaturesMixin):
    __abstract__ = True


BaseModel.set_session(db.session)


def create_uiid() -> str:
    return str(uuid4())


class PetModel(BaseModel):
    __tablename__ = "pets"

    uuid: orm.Mapped[str] = orm.mapped_column(primary_key=True, default=create_uiid)
    pet_image: orm.Mapped[str] = orm.mapped_column(sa.Text)
    pet_type: orm.Mapped[str] = orm.mapped_column(sa.String(10))
    breed: orm.Mapped[str] = orm.mapped_column(sa.String(20))
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    age: orm.Mapped[int]
    owner_id: orm.Mapped[str] = orm.mapped_column(sa.Text, sa.ForeignKey("users.uuid"))


class UserModel(BaseModel):
    __tablename__ = "users"

    uuid: orm.Mapped[str] = orm.mapped_column(primary_key=True, default=create_uiid)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(100))
    address: orm.Mapped[str] = orm.mapped_column(sa.String(255))
    contact_number: orm.Mapped[str] = orm.mapped_column(sa.String(13))
    email: orm.Mapped[str] = orm.mapped_column(sa.String(255), unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sa.Text)
    image: orm.Mapped[str] = orm.mapped_column(sa.Text)
    gender: orm.Mapped[str] = orm.mapped_column(sa.String(25))
    age: orm.Mapped[int] = orm.mapped_column(sa.Integer)

    pets = orm.relationship(
        "PetModel", backref="owner", cascade="all, delete", lazy="dynamic"
    )
    notifications = orm.relationship(
        "NotificationModel", backref="dynamic", cascade="all, delete", lazy="dynamic"
    )


class NotificationModel(BaseModel):
    __tablename__ = "notifications"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[str] = orm.mapped_column(sa.Text, sa.ForeignKey("users.uuid"))
    pet_id: orm.Mapped[str] = orm.mapped_column(sa.Text, sa.ForeignKey("pets.uuid"))
    created_at = sa.Column(
        sa.DateTime,
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=8),
    )
    latitude: orm.Mapped[float]
    longitude: orm.Mapped[float]
    pet = orm.relationship("PetModel")
