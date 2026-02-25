from flask import request, abort

from app import db
from app.models import Todo


class UserTodoVisibilityMixin:
    """ Mixin for retrieving only user todos
    """

    def get_query(self):
        return db.select(Todo).filter_by(user=request.user)

    def get_todo_or_404(self, todo_id):
        stmt = self.get_query().filter_by(id=todo_id)
        todo = db.session.scalars(stmt).first()
        if not todo:
            abort(404, "Not found")
        return todo
