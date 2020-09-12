from mongoengine import Document
from core.custom_query_set import CustomQuerySet

class CustomDocument(Document):
    meta = {'allow_inheritance': True}

    def to_mongo(self):
        document = super().to_mongo()
        document['_id'] = str(document['_id'])

        return document

