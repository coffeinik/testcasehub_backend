from flask import Flask, Blueprint
from flask_restx import Api, Namespace, fields, Resource

from .models import TODOS


api = Namespace("suites", description="Suites operations")

suite = api.model(
    "Suite", {"name": fields.String(required=True, description="The suite name")}
)

listed_suite = api.model(
    "ListedSuite",
    {
        "id": fields.String(required=True, description="The suite ID"),
        "suite": fields.Nested(suite, description="The Suite"),
    },
)


def abort_if_suite_doesnt_exist(suite_id):
    if suite_id not in TODOS:
        api.abort(404, "Suite {} doesn't exist".format(suite_id))


@api.route("/<string:suite_id>")
@api.doc(responses={404: "Suite not found"}, params={"suite_id": "The Suite ID"})
class Suite(Resource):
    """Show a single suite item and lets you delete them"""

    @api.doc(description="suite_id should be in {0}".format(", ".join(TODOS.keys())))
    @api.marshal_with(suite)
    def get(self, suite_id):
        """Fetch a given resource"""
        abort_if_suite_doesnt_exist(suite_id)
        return TODOS[suite_id]

    @api.doc(responses={204: "Suite deleted"})
    def delete(self, suite_id):
        """Delete a given resource"""
        abort_if_suite_doesnt_exist(suite_id)
        del TODOS[suite_id]
        return "", 204

    @api.doc()
    @api.marshal_with(suite)
    def put(self, suite_id):
        """Update a given resource"""
        task = {"task": "task"}
        TODOS[suite_id] = task
        return task


@api.route("/")
class SuiteList(Resource):
    """Shows a list of all suites, and lets you POST to add new tasks"""

    @api.marshal_list_with(listed_suite)
    def get(self):
        """List all suites"""
        return [{"id": id, "suite": suite} for id, suite in TODOS.items()]

    @api.doc()
    @api.marshal_with(suite, code=201)
    def post(self):
        """Create a suite"""
        suite_id = "suite%d" % (len(TODOS) + 1)
        TODOS[suite_id] = {"task": "task"}
        return TODOS[suite_id], 201