from mongoengine import Document, StringField, DateField, EmbeddedDocumentListField
from core.custom_query_set import CustomQuerySet

from models.membership import Membership

class Athlete(Document):
    meta = {'queryset_class' : CustomQuerySet }

    name            = StringField(required=True)
    last_name       = StringField(required=True)
    birth_date      = DateField(required=True)
    birth_place      = StringField(required=True)
    fiscal_code     = StringField(required=True)
    address         = StringField(required=True)
    zip_code        = StringField(required=True, max_length=5)
    city            = StringField(required=True)
    province        = StringField(required=True, max_length=2)
    gender          = StringField(required=True, max_length=1)
    phone           = StringField(required=True)
    email           = StringField(required=True)
    memberships     = EmbeddedDocumentListField(Membership)

    def jsonify(self):
        document = super().to_mongo()
        if "_id" in document:
            document['_id'] = str(document['_id'])

        return document