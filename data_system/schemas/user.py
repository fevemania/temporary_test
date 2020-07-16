from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        ordered = True

    unique_id = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    totp_codes = fields.List(fields.String(required=True, load_only=True), required=True, load_only=True)
#    created_at = fields.DateTime(dump_only=True)
#    updated_at = fields.DateTime(dump_only=True)
