from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import asc, desc

bp = Blueprint('todos', __name__, url_prefix="/todos", description="Todo API")

from app import db
from app.decorators import token_required
from app.helpers import add_pagination_to_response
from app.models import Todo
from app.todos.mixins import UserTodoVisibilityMixin
from app.todos.schemas import (
    TodoCreateRequestSchema,
    TodoUpdateRequestSchema,
    TodoSchema,
    ListTodosSchema)
from app.todos.filters import ListTodosParameters


@bp.route("/")
class TodoListView(UserTodoVisibilityMixin, MethodView):
    @bp.arguments(ListTodosParameters, location="query")
    @bp.response(status_code=200, schema=ListTodosSchema)
    @token_required
    def get(self, parameters):
        """ List all Todos
        """
        page = parameters['page']
        order_by = parameters['order_by']
        order_func = asc if parameters['order'].value == 'asc' else desc

        stmt = self.get_query().order_by(order_func(order_by.value))

        if 'search' in parameters:
            stmt = stmt.filter(Todo.content.like("{}%".format(parameters['search'])))

        todos = db.paginate(stmt, page=page, per_page=current_app.config['DEFAULT_PAGINATION_COUNT'], error_out=False)

        response = add_pagination_to_response({"todos": todos}, 'todos.TodoListView', todos)
        return response

    @bp.arguments(TodoCreateRequestSchema)
    @bp.response(status_code=201, schema=TodoSchema)
    @token_required
    def post(self, todo_data):
        """ Create a new Todo
        """
        todo = Todo(**todo_data, user=request.user)
        db.session.add(todo)
        db.session.commit()
        return todo


@bp.route("/<int:todo_id>")
class TodoView(UserTodoVisibilityMixin, MethodView):
    @bp.response(status_code=200, schema=TodoSchema)
    @token_required
    def get(self, todo_id):
        """ Get a single Todo
        """
        todo = self.get_todo_or_404(todo_id)
        return todo

    @bp.arguments(TodoUpdateRequestSchema)
    @bp.response(status_code=200, schema=TodoSchema)
    @token_required
    def put(self, payload, todo_id):
        """ Update existing Todo
        """
        todo = self.get_todo_or_404(todo_id)
        todo.done = payload.get('done', todo.done)
        todo.content = payload.get('content', todo.content)
        db.session.commit()
        return todo

    @bp.response(status_code=204)
    @token_required
    def delete(self, todo_id):
        """ Delete a Todo
        """
        todo = self.get_todo_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
