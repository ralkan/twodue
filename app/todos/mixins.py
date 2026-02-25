from flask import request, abort

from app import db
from app.models import Todo


class UserTodoVisibilityMixin:
    """
    A mixin for retrieving only user todos.

    This way, you can't forget to filter on the user todo's
    and accidentally expose other users' todo's which the current user
    is not supposed to see and/or interact with.
    """

    def get_query(self):
        """ Return the pre filtered query/stmt
        """
        return db.select(Todo).filter_by(user=request.user)

    def get_todo_or_404(self, todo_id):
        """
        Using the pre filtered query find a todo by id.
        Early return a 404 if not found
        """
        stmt = self.get_query().filter_by(id=todo_id)
        todo = db.session.scalars(stmt).first()
        if not todo:
            abort(404, "Not found")
        return todo
