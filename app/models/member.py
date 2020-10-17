from mongoengine import Document, StringField, DateField, EmailField, EmbeddedDocumentListField
from core.custom_query_set import CustomQuerySet

from models.membership import Membership

from typing import Optional

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
    memberships     = EmbeddedDocumentListField(Membership)

    def get_latest_membership(self) -> Optional[DateField]:

        if(len(self.memberships) == 0): return None
        if( len(self.memberships) == 1): return self.memberships[0].end_date

        latest_membership = self.memberships[0].end_date
        for membership in self.memberships:
            if(membership.end_date > latest_membership): latest_membership = membership.end_date

        return latest_membership

    def jsonify(self):
        document = super().to_mongo()
        if "_id" in document:
            document['_id'] = str(document['_id'])

        return document

