from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    api_v1 = Blueprint("api", __name__, url_prefix="/api/1")
    api = Api(api_v1, version="1.0", title="CaseHub Backend API", description="",)

    from .cases.resources import api as cases_api
    from .suites.resources import api as suites_api
    api.add_namespace(cases_api)
    api.add_namespace(suites_api)

    app.register_blueprint(api_v1)
    return app


if __name__ == "__main__":
    app = create_app("config.yaml")
    app.run(host="0.0.0.0", port=8000, debug=True)