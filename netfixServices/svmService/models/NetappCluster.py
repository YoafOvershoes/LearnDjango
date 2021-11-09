from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty, BooleanProperty, RelationshipTo, RelationshipFrom, \
    Relationship, config


# config.DATABASE_URL = 'bolt://neo4j:shMador1@localhost:7687' another way to set the db not in the app settings


class NetappCluster(StructuredNode):
    name = StringProperty(unique_index=True)
    mgmtAddress = StringProperty(max_length=16)

    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,
                'mgmtAddress': self.mgmtAddress,
            },
        }
