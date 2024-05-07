from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_kwargs
from werkzeug.security import check_password_hash, generate_password_hash

from qrcollarcompanion_api.config import BASE_DIR
from qrcollarcompanion_api.models import NotificationModel, PetModel, UserModel
from qrcollarcompanion_api.schemas import (
    CreateNotificationSchema,
    NotificationSchema,
    PetSchema,
    RegisterUserSchema,
    UserSchema,
)


class PetResource(MethodView):
    def get(self, uuid: str):
        pet = PetModel.find_or_fail(uuid)
        return {
            "pet": PetSchema().dump(pet),
        }

    @jwt_required()
    def put(self, uuid: str):
        raise NotImplementedError

    @jwt_required()
    def delete(self, uuid: str):
        pet = PetModel.find(uuid)
        pet.delete()

        return "", 204


class NotificationResource(MethodView):
    def post(self, uuid):
        pet = PetModel.find_or_fail(uuid)
        try:
            data = CreateNotificationSchema().load(request.get_json())
            NotificationModel.create(
                pet_id=pet.uuid,
                user_id=pet.owner_id,
                latitude=data["latitude"],
                longitude=data["longitude"],
                message=data["message"],
            )

            return "", 204
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400


class PetListResource(MethodView):
    @jwt_required()
    def get(self):
        user = UserModel.find(get_jwt_identity())
        pets = PetSchema(many=True).dump(user.pets.all())

        return jsonify({"pets": pets})

    @jwt_required()
    def post(self):
        try:
            user = UserModel.find(get_jwt_identity())
            data = PetSchema().load(request.get_json())
            PetModel.create(
                pet_image=data["pet_image"],
                pet_type=data["pet_type"],
                breed=data["breed"],
                name=data["name"],
                age=data["age"],
                owner_id=user.uuid,
            )

            return "", 204
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400


class NotificationListResource(MethodView):
    @jwt_required()
    def get(self):
        current_user = UserModel.find(get_jwt_identity())
        notifications = NotificationModel.query.filter_by(user_id=current_user.uuid).group_by(NotificationModel.created_at).all()
        data = NotificationSchema(many=True).dump(notifications)

        return jsonify({"notifications": data})


class CurrentUserEndpoint(MethodView):
    @jwt_required()
    def get(self):
        current_user = UserModel.find(get_jwt_identity())
        return jsonify(current_user=UserSchema().dump(current_user))

    @jwt_required()
    def put(self):
        current_user = UserModel.find(get_jwt_identity())
        data = UserSchema().dump(request.get_json())

        try:
            current_user.update(**data)
            return "", 204
        except IntegrityError:
            return jsonify({"errors": {"email": "Email is already in use."}})

    @jwt_required()
    def delete(self):
        current_user = UserModel.find(get_jwt_identity())
        current_user.delete()

        return "", 204


class RegisterEndpoint(MethodView):
    def post(self):
        try:
            data = RegisterUserSchema().load(request.get_json())
            user = UserModel.create(
                name=data["name"],
                address=data["address"],
                contact_number=data["contact_number"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                image=data["image"],
                age=data["age"],
                gender=data["gender"],
            )
            access_token = create_access_token(user.uuid)

            return jsonify(access_token=access_token)

        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        except IntegrityError:
            return jsonify({"errors": {"email": "Email is alread in use."}})


class SignInEndpoint(MethodView):
    @use_kwargs(
        {
            "email": fields.Email(required=True),
            "password": fields.Str(required=True),
        },
        location="json",
    )
    def post(self, email: str, password: str):
        user = UserModel.where(email=email).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.uuid)
            return jsonify(access_token=access_token)

        return jsonify({"errors": {"email": "Wrong email or password."}}), 401
