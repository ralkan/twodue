from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Todo(db.Model):
    # Use UUID but keep Int for assessment simplicity
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255), index=True)
    done: Mapped[bool] = mapped_column(Boolean(), default=False)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return '<Todo {}: {}>'.format(self.content, self.done)


class User(db.Model):
    # Use UUID but keep Int for assessment simplicity
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(), unique=True)

    todos: Mapped[List["Todo"]] = relationship(backref="user")

    def __repr__(self):
        return '<User ({}): {}>'.format(self.id, self.email)
