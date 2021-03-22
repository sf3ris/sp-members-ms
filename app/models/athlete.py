from mongoengine import (
    Document,
    StringField,
    DateField,
    EmbeddedDocumentListField
)
from core.custom_query_set import CustomQuerySet

from models.membership import Membership


class Athlete(Document):
    meta = {'queryset_class': CustomQuerySet}

    name = StringField(required=True)
    last_name = StringField(required=True)
    birth_date = DateField(required=True)
    birth_place = StringField(required=True)
    fiscal_code = StringField(required=True)
    address = StringField(required=True)
    zip_code = StringField(required=True, max_length=5)
    city = StringField(required=True)
    province = StringField(required=True, max_length=2)
    gender = StringField(required=True, max_length=1)
    phone = StringField(required=True)
    email = StringField(required=True)
    memberships = EmbeddedDocumentListField(Membership)

    def jsonify(self):
        document = super().to_mongo()
        if "_id" in document:
            document['_id'] = str(document['_id'])

        return document

    def is_empty(self):
        return not self.name \
               and not self.last_name \
               and not self.birth_date \
               and not self.birth_place \
               and not self.fiscal_code \
               and not self.address \
               and not self.city \
               and not self.email \
               and not self.province \
               and not self.gender \
               and not self.email
