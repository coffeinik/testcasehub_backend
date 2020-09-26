from mongoengine import Document, StringField


class ProjectModel(Document):
    name = StringField(max_length=200, required=True)
