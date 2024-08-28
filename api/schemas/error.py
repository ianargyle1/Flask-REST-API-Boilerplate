from marshmallow import Schema, fields


class ErrorSchema(Schema):
    message = fields.Str(required=True)

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def to_dict(self):
        return self.dump(self)
