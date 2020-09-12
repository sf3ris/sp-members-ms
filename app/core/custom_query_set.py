from mongoengine import QuerySet
from sys import stderr

class CustomQuerySet(QuerySet):

    def load(self):
        queryset = super().all()

        print(queryset, file=stderr)

        return list(
            map( lambda document: document.to_mongo(), queryset)
        )