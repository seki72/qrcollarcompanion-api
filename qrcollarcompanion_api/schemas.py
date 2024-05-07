from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    uuid = fields.Str(dump_only=True)
    name = fields.Str()
    address = fields.Str()
    contact_number = fields.Str()
    email = fields.Str()
    image = fields.Str()
    gender = fields.Str()
    age = fields.Str()


class PetSchema(Schema):
    uuid = fields.Str(dump_only=True)
    pet_image = fields.Str()
    pet_type = fields.Str()
    breed = fields.Str()
    name = fields.Str(required=True)
    age = fields.Int(as_string=True)
    owner = fields.Nested(UserSchema)


class NotificationSchema(Schema):
    pet = fields.Nested(PetSchema)
    created_at = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    message = fields.Str()


class CreateNotificationSchema(Schema):
    pet_id = fields.Int()
    latitude = fields.Float()
    longitude = fields.Float()
    message = fields.Str()


class RegisterUserSchema(Schema):
    name = fields.Str()
    address = fields.Str()
    contact_number = fields.Str()
    email = fields.Email()
    password = fields.Str()
    image = fields.Str()
    gender = fields.Str()
    age = fields.Str() # If gikan sa frontend, ang age kay string
