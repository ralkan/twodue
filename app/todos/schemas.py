from marshmallow import Schema, fields


class TodoCreateRequestSchema(Schema):
    content = fields.Str(required=True)
    done = fields.Bool(required=False)


class TodoSchema(TodoCreateRequestSchema):
    id = fields.Int()


class ListTodosSchema(Schema):
    todos = fields.List(fields.Nested(TodoSchema))
