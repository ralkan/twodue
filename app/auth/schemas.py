""" Request and Response schema's (serializers) for Auth are defined here
"""
from marshmallow import Schema, fields


class LoginRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class RegisterRequestSchema(LoginRequestSchema):
    name = fields.Str(required=True)


class UserSchema(RegisterRequestSchema):
    id = fields.Int()
    token = fields.Str(required=False)
