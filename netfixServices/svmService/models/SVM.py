from django.core.serializers.json import DjangoJSONEncoder

from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty, BooleanProperty, RelationshipTo, RelationshipFrom, \
    Relationship

from svmService.models import SVM
from .NetappCluster import NetappCluster
from .DrRel import DataRecoveryRelation
from .SvmClusterRel import SvmInClusterRel
from .NodeUtils import NodeUtils


class SVM(StructuredNode):
    # Properties
    name = StringProperty(unique_index=True)
    is_active = BooleanProperty(default=True)
    environment = StringProperty()
    site = StringProperty()
    # Relationships
    inCluster = RelationshipTo(NetappCluster, 'InCluster', model=SvmInClusterRel)
    drSVM = RelationshipTo('SVM', 'DataRecovery', model=DataRecoveryRelation)

    # Serializing the svm node, because noemodel doesn't have a serializeable built in function
    @property
    def serialize(self):
        return {
            self.name: {  # used to be "node_properties"
                'node_id': self.id,
                'name': self.name,
                'isActive': self.is_active,
                'DrRelation': self.svm_data_recovery_serializer,
                'ClusterRelation': self.svm_in_cluster_serializer
                # 'inCluster': self.inCluster,
                # 'drRelation': self.drSVM.start_node()
            },
        }

    # TODO: make this function simpler
    @property
    def svm_data_recovery_serializer(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)=$self MATCH (a)-[r: DataRecovery]->(b) RETURN b")
        query_result = [self.inflate(row[0]) for row in results]


        # data_recovery = []# TODO: if svm can have 2 relations return array
        # for node in query_result:
        #     print(node)
        #     data_recovery.append(
        #         {
        #             # enter properties here
        #             'drSvm': node.serialize
        #         }
        #     )

        data_recovery = {}
        if query_result.__len__() > 0:
            data_recovery = {
                # relation's properties
                'drSvm': query_result[0].serialize  # get the relationship end node, and serialize him
            }
        return data_recovery
        # return {
        #     'nodes_related': self.serialize_relationships(SVM.nodes.all()),
        # }

    @property
    def svm_in_cluster_serializer(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)=$self MATCH (a)-[r: InCluster]->(b: NetappCluster) "
                                       "RETURN b")
        query_result = [NetappCluster.inflate(row[0]) for row in results]
        cluster = {}
        if query_result.__len__() > 0:
            cluster = {
                # relation's properties
                'cluster': query_result[0].serialize  # get the relationship end node, and serialize him
            }
        return cluster
