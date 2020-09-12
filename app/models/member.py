from mongoengine import Document, StringField, DateField, EmailField
from core.custom_document import CustomDocument
from core.custom_query_set import CustomQuerySet

class Member(Document):
    meta = {'queryset_class': CustomQuerySet}

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

    def to_mongo(self):
        document = super().to_mongo()
        document['_id'] = str(document['_id'])

        return document


