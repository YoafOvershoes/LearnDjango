from django.core.serializers.json import DjangoJSONEncoder

from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty, BooleanProperty, RelationshipTo, RelationshipFrom, \
    Relationship

from svmService.models import SVM
from .NetappCluster import NetappCluster
from .DrRel import DataRecoveryRelation
from .NodeUtils import NodeUtils


class SVM(StructuredNode, NodeUtils):
    name = StringProperty(unique_index=True)
    is_active = BooleanProperty(default=True)
    inCluster = RelationshipTo(NetappCluster, 'inCluster')
    drSVM = RelationshipTo(SVM, 'DataRecovery', model=DataRecoveryRelation)

    # Serializing the svm node, because noemodel doesn't have a serializeable built in function
    @property
    def serialize(self):
        return {
            self.name: { # used to be "node_properties"
                'node_id': self.id,
                'name': self.name,
                'isActive': self.is_active,
                # 'inCluster': self.inCluster,
                #'drRelation': self.drSVM.start_node()
            },
        }

    @property
    def serialize_collection(self):
        return {
            'nodes_related': self.serialize_relationships(SVM.nodes.all()),
        }
