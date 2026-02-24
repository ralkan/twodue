from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Todo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255), index=True)
    done: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __repr__(self):
        return '<Todo {}: {}>'.format(self.content, self.done)
