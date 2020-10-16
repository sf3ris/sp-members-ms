from mongoengine import EmbeddedDocument, DateField

class Membership(EmbeddedDocument):

    start_date  = DateField(required=True)
    end_date    = DateField(required=True)    