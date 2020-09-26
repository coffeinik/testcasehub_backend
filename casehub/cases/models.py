from mongoengine import Document, StringField


class CaseModel(Document):
    title = StringField(max_length=200, required=True)

    
TODOS = {
    "case1": {"task": "build an API"},
    "case2": {"task": "?????"},
    "case3": {"task": "profit!"},
}

