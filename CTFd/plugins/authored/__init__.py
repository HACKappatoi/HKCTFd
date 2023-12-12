from flask import Blueprint

from CTFd.models import Challenges, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.migrations import upgrade


class AuthoredChallengeModel(Challenges):
    __mapper_args__ = {"polymorphic_identity": "authored"}
    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )
    author = db.Column(db.String(32), default='unknown')


    def __init__(self, *args, **kwargs):
        super(AuthoredChallengeModel, self).__init__(**kwargs)


class AuthoredChallenge(BaseChallenge):
    id = "authored"  # Unique identifier used to register challenges
    name = "authored"  # Name of a challenge type
    templates = (
        {  # Handlebars templates used for each aspect of challenge editing & viewing
            "create": "/plugins/authored/assets/create.html",
            "update": "/plugins/authored/assets/update.html",
            "view": "/plugins/authored/assets/view.html",
        }
    )
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/authored/assets/create.js",
        "update": "/plugins/authored/assets/update.js",
        "view": "/plugins/authored/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/authored/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "authored",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )
    challenge_model = AuthoredChallengeModel

    @classmethod
    def read(cls, challenge):
        """
        This method is in used to access the data of a challenge in a format processable by the front end.

        :param challenge:
        :return: Challenge object, data dictionary to be returned to the user
        """
        challenge = AuthoredChallengeModel.query.filter_by(id=challenge.id).first()
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "value": challenge.value,
            "author": challenge.author,
            "description": challenge.description,
            "connection_info": challenge.connection_info,
            "next_id": challenge.next_id,
            "category": challenge.category,
            "state": challenge.state,
            "max_attempts": challenge.max_attempts,
            "type": challenge.type,
            "type_data": {
                "id": cls.id,
                "name": cls.name,
                "templates": cls.templates,
                "scripts": cls.scripts,
            },
        }
        return data



def load(app):
    app.db.create_all()
    upgrade(plugin_name="authored")
    CHALLENGE_CLASSES["authored"] = AuthoredChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/authored/assets/"
    )
