from flask import Flask, Blueprint
from mongoengine.errors import DoesNotExist
from flask_restx import Api, Resource, fields, Namespace

from .models import ProjectModel
from .forms import project_request_fields, project_response_fields


api = Namespace('projects')


def abort_if_project_doesnt_exist(project_id):
    api.abort(404, "Project {} doesn't exist".format(project_id))



@api.route('/<string:project_id>')
@api.doc(responses={404: 'Project not found'}, params={'project_id': 'The Project ID'})
class Project(Resource):
    '''Show a single project item and lets you delete them'''

    @api.doc(description='#TODO')
    @api.marshal_with(project_response_fields)
    def get(self, project_id):
        '''Fetch a given resource'''

        try:
            project_model = ProjectModel.objects.get(id=project_id)
        except DoesNotExist:
            abort_if_project_doesnt_exist(project_id)
        return project_model

    @api.doc("#TODO")
    @api.response(204, "Project deleted")
    def delete(self, project_id):
        """Delete a project given its identifier"""
        
        try:
            project_model = ProjectModel.objects.get(id=project_id)
        except DoesNotExist:
            abort_if_project_doesnt_exist(project_id)
        project_model.delete()
        return '', 204

    @api.expect(project_request_fields)
    @api.marshal_with(project_response_fields)
    def put(self, project_id):
        """Update a project given its identifier"""

        try:
            project_model = ProjectModel.objects.get(id=project_id)
        except DoesNotExist:
            abort_if_project_doesnt_exist(project_id)

        project_model.update(**api.payload)
        project_model.reload()
        return project_model


@api.route('/')
class ProjectList(Resource):
    '''Shows a list of all projects, and lets you POST to add new projects'''

    @api.doc(description='#TODO')
    @api.marshal_list_with(project_response_fields)
    def get(self):
        '''List all projects'''

        return list(ProjectModel.objects.all())

    @api.doc()
    @api.expect(project_request_fields)
    @api.marshal_with(project_response_fields, code=201)
    def post(self):
        '''Create a project'''

        project_model = ProjectModel(**api.payload).save()
        return project_model, 201
