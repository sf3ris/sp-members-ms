from mongoengine import EmbeddedDocument, DateField, ObjectIdField, StringField
from bson.objectid import ObjectId

class Membership(EmbeddedDocument):
    _id         = StringField( required=True, default= lambda: str(ObjectId()))
    start_date  = DateField(required=True)
    end_date    = DateField(required=True)  