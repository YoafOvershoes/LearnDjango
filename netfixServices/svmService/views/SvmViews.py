import json
from django import forms

from django.http import JsonResponse
from django.core.serializers import serialize

from django.views.decorators.csrf import csrf_exempt

from neomodel import *
from svmService.models.NetappCluster import NetappCluster
from svmService.models.SVM import SVM
from svmService.models.DrRel import DataRecoveryRelation


@csrf_exempt
def get_all_svm(request):
    if request.method == 'GET':
        svms = SVM.nodes.all()
        svm_json = []

        for svm in svms:
            svm_json.append(svm.serialize)

        return JsonResponse(svm_json, safe=False)


@csrf_exempt
def create(request):
    if request.method == 'POST':
        f_bool = forms.BooleanField()  # A cool way to check fields and clean them, without doing much logic or switch case!
        svm_json = json.loads(request.body.decode('utf-8'))
        svm_name = svm_json['name'].lower()
        is_active = f_bool.clean(svm_json['isActive'])
        response = {"error": "Could not save node"}
        svm = SVM(name=svm_name, is_active=is_active)

        # check if svm doesnot exist - unique_index does not work!!!! :(
        svm_exist = True
        try:
            svm = SVM.nodes.get(name=svm_name)
        except SVM.DoesNotExist:
            svm_exist = False

        try:

            if svm_exist == False:
                svm = SVM(name=svm_name, is_active=is_active)
                svm.save()
                response = {"id": svm.id}
            else:
                response = {"id": svm.id, "misconfiguration": "svm already exists"}

        except:
            print("could not save svm: ")
            print(svm.serialize)

        return JsonResponse(response)

    return JsonResponse('not from get_all_node', safe=False)


@csrf_exempt
# get 2 svm names, src and dr
# change the dr svm to active false
# creates an DataRecovery Relation
def connect(request):
    if request.method == 'POST':
        connection_json = json.loads(request.body.decode('utf-8'))
        svm_src_name = connection_json['source'].lower()
        svm_dr_name = connection_json['destination'].lower()

        try:
            svm_src = SVM.nodes.get(name=svm_src_name)
            svm_dr = SVM.nodes.get(name=svm_dr_name)
        except SVM.DoesNotExist:
            print("Couldn't find one of the svm")
            return JsonResponse(status=500)

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
