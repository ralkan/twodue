""" Request and Response schema's (serializers) are defined here
"""
from marshmallow import Schema, fields, validates_schema, ValidationError


class TodoCreateRequestSchema(Schema):
    content = fields.Str(required=True)
    done = fields.Bool(required=False)


class TodoUpdateRequestSchema(TodoCreateRequestSchema):
    # Same as request schema but required = False
    content = fields.Str(required=False)

    @validates_schema
    def validate_all_fields(self, data, **kwargs):
        if not data:
            raise ValidationError('At least one of the parameters "content" or "done" should be provided')


class TodoSchema(TodoCreateRequestSchema):
    id = fields.Int()


class ListTodosSchema(Schema):
    todos = fields.List(fields.Nested(TodoSchema))
