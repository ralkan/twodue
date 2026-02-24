from flask.views import MethodView
from flask_smorest import Blueprint

bp = Blueprint('todos', __name__, url_prefix="/todos", description="Todo API")

from app import db
from app.models import Todo
from app.todos.schemas import TodoCreateRequestSchema, TodoSchema, ListTodosSchema
from app.todos.filters import ListTodosParameters


@bp.route("/")
class TodoListView(MethodView):
    @bp.arguments(ListTodosParameters, location="query")
    @bp.response(status_code=200, schema=ListTodosSchema)
    def get(self, parameters):
        # TODO: order by
        todos = Todo.query.all()
        return {"todos": todos}

    @bp.arguments(TodoCreateRequestSchema)
    @bp.response(status_code=201, schema=TodoSchema)
    def post(self, todo_data):
        todo = Todo(**todo_data)
        db.session.add(todo)
        db.session.commit()
        return todo


@bp.route("/<int:todo_id>")
class TodoView(MethodView):
    @bp.response(status_code=200, schema=TodoSchema)
    def get(self, todo_id):
        todo = Todo.query.get_or_404(todo_id)
        return todo

    @bp.arguments(TodoCreateRequestSchema)
    @bp.response(status_code=200, schema=TodoSchema)
    def put(self, payload, todo_id):
        todo = Todo.query.get_or_404(todo_id)
        todo.done = payload.get('done', todo.done)
        todo.content = payload.get('content', todo.content)
        db.session.commit()
        return todo

    @bp.response(status_code=204)
    def delete(self, todo_id):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
