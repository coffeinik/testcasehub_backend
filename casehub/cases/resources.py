from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields, Namespace

from .models import TODOS

api = Namespace("cases", description="TODO operations")

case = api.model(
    "Case", {"task": fields.String(required=True, description="The task details")}
)

listed_case = api.model(
    "ListedCase",
    {
        "id": fields.String(required=True, description="The case ID"),
        "case": fields.Nested(case, description="The Case"),
    },
)


def abort_if_case_doesnt_exist(case_id):
    if case_id not in TODOS:
        api.abort(404, "Case {} doesn't exist".format(case_id))



@api.route("/<string:case_id>")
@api.doc(responses={404: "Case not found"}, params={"case_id": "The Case ID"})
class Case(Resource):
    """Show a single case item and lets you delete them"""

    @api.doc(description="case_id should be in {0}".format(", ".join(TODOS.keys())))
    @api.marshal_with(case)
    def get(self, case_id):
        """Fetch a given resource"""
        abort_if_case_doesnt_exist(case_id)
        return TODOS[case_id]

    @api.doc(responses={204: "Case deleted"})
    def delete(self, case_id):
        """Delete a given resource"""
        abort_if_case_doesnt_exist(case_id)
        del TODOS[case_id]
        return "", 204

    @api.doc()
    @api.marshal_with(case)
    def put(self, case_id):
        """Update a given resource"""
        task = {"task": "test"}
        TODOS[case_id] = task
        return task


@api.route("/")
class CaseList(Resource):
    """Shows a list of all cases, and lets you POST to add new tasks"""

    @api.marshal_list_with(listed_case)
    def get(self):
        """List all cases"""
        return [{"id": id, "case": case} for id, case in TODOS.items()]

    @api.doc()
    @api.marshal_with(case, code=201)
    def post(self):
        """Create a case"""
        case_id = "case%d" % (len(TODOS) + 1)
        TODOS[case_id] = {"task": "task"}
        return TODOS[case_id], 201