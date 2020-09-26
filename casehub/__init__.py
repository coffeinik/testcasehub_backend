from flask import Flask, Blueprint
from flask_mongoengine import MongoEngine
from flask_restx import Api


def create_app(config_filename='config.yaml', debug=True):
    app = Flask(__name__)

    app.config.from_pyfile(config_filename)

    api_v1 = Blueprint("api", __name__, url_prefix="/api/1")
    api = Api(api_v1, version="1.0", title="CaseHub Backend API", description="#TODO",)
    
    db = MongoEngine()
    db.init_app(app)

    from .cases.resources import api as cases_api
    from .suites.resources import api as suites_api
    from .projects.resources import api as projects_api
    api.add_namespace(cases_api)
    api.add_namespace(suites_api)
    api.add_namespace(projects_api)

    app.register_blueprint(api_v1)
    return app