import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from qrcollarcompanion_api.api import (
    CurrentUserEndpoint,
    NotificationResource,
    NotificationListResource,
    PetListResource,
    PetResource,
    RegisterEndpoint,
    SignInEndpoint,
)
from qrcollarcompanion_api.config import BASE_DIR
from qrcollarcompanion_api.models import db

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY=os.environ["SECRET_KEY"],
    JWT_SECRET_KEY=os.environ["SECRET_KEY"],
    JWT_ACCESS_TOKEN_EXPIRES=False,
    SQLALCHEMY_DATABASE_URI="sqlite:///database.sqlite",
    UPLOAD_FOLDER=os.path.join(BASE_DIR, "uploads"),
)

db.init_app(app)
Migrate(app, db)
JWTManager(app)

app.add_url_rule("/api/v1/login", view_func=SignInEndpoint.as_view("login"))
app.add_url_rule("/api/v1/register", view_func=RegisterEndpoint.as_view("register"))
app.add_url_rule("/api/v1/pets", view_func=PetListResource.as_view("pet_list"))
app.add_url_rule("/api/v1/pets/<uuid>", view_func=PetResource.as_view("pet"))
app.add_url_rule("/api/v1/user", view_func=CurrentUserEndpoint.as_view("current_user"))
app.add_url_rule(
    "/api/v1/notifications",
    view_func=NotificationListResource.as_view("notification_list"),
)
app.add_url_rule(
    "/api/v1/pets/<uuid>/notify", view_func=NotificationResource.as_view("notify")
)

# Test endpoint
@app.route("/")
def welcome():
    return "Welcome to QRCollarCompanion!"
