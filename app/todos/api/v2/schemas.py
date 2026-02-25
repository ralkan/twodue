""" Request and Response schema's (serializers) for Todos are defined here
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
        # Validate both content and done values as we need at least one of the two in the request body
        if not data:
            raise ValidationError('At least one of the parameters "content" or "done" should be provided')


class TodoSchema(TodoCreateRequestSchema):
    id = fields.Int()


class ListTodosSchema(Schema):
    total_records = fields.Int(required=False)
    total_pages = fields.Int(required=False)
    next = fields.Str(required=False)
    prev = fields.Str(required=False)
    todos = fields.List(fields.Nested(TodoSchema))
