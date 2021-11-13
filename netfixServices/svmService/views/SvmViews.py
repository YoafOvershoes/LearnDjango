import json
from django import forms

from django.http import JsonResponse
from django.core.serializers import serialize

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from neomodel import *
from svmService.models.NetappCluster import NetappCluster
from svmService.models.SVM import SVM
from svmService.models.DrRel import DataRecoveryRelation
import environ

env = environ.Env()
environ.Env.read_env()


@csrf_exempt
@require_http_methods(["GET"])
def get_all_svm(request):
    svms = SVM.nodes.all()
    svm_json = []

    for svm in svms:
        svm_json.append(svm.serialize)

    return JsonResponse(svm_json, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    # get data from json
    f_bool = forms.BooleanField()  # A cool way to check fields and clean them, without doing much logic or switch case!
    svm_json = json.loads(request.body.decode('utf-8'))
    svm_name = svm_json['name'].lower()
    is_active = f_bool.clean(svm_json['isActive'])
    site = svm_json['site'].lower()
    environment = svm_json['environment'].upper()
    # default response
    response = {"error": "Could not save node"}

    #  svm = SVM(name=svm_name, is_active=is_active)

    # check if svm doesn't exist - unique_index does not work!!!! :(
    svm_exist = True
    try:
        # svm = SVM.nodes.get(name=svm_name) # why would create get an already existing node?
        svm = SVM(name=svm_name, is_active=is_active, environment=environment, site=site)
        # svm.create_or_update() # TODO: CHECK WHY IT DOES NOT WORK!
        svm.save()
        response = {"id": svm.id}
        print(env(environment + "_" + site))
    except SVM.DoesNotExist:
        return JsonResponse({"error": "svm does not exist!"})
    except:
        print("could not save svm")
        print(svm.serialize)
    return JsonResponse(response)


# get 2 svm names, src and dr
# change the dr svm to active false
# creates an DataRecovery Relation
@csrf_exempt
@require_http_methods(["POST"])
def connect_nodes_to_dr(request):
    connection_json = json.loads(request.body.decode('utf-8'))
    svm_src_name = connection_json['source'].lower()
    svm_dr_name = connection_json['destination'].lower()

    try:
        svm_src = SVM.nodes.get(name=svm_src_name)
        svm_dr = SVM.nodes.get(name=svm_dr_name)
    except SVM.DoesNotExist:
        print("Couldn't find one of the svm")
        return JsonResponse(data={'error': 'svm does not exist'}, status=404)

    # check if non of the relation ships exist

    relation_from_src_to_dest = svm_src.drSVM.relationship(svm_dr)
    relation_from_dest_to_src = svm_dr.drSVM.relationship(svm_src)

    if relation_from_src_to_dest is None and relation_from_dest_to_src is None:
        svm_dr.is_active = False
        svm_dr.save()  # save the changes

        dr_rel = svm_src.drSVM.connect(svm_dr)
        dr_rel.since
        dr_rel.save()
    else:
        return JsonResponse({"misconfiguration": "relationship already exist between the nodes"})

    return JsonResponse(svm_src.serialize)
