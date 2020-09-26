from flask_restx import fields


project_request_fields = {
    'name': fields.String(required=True, description='Project name'),
}


project_response_fields = {
    'id': fields.String(required=False, description='Project id', attribute='pk'),
    'name': fields.String(required=True, description='Project name'),
}
