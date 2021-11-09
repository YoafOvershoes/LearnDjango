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

        # create new node
        # bom0 = NetappCluster(name='ht9540bom0nac1', mgmtAddress='1.1.1.1')
        # bom0.save()

        for svm in svms:
            svm_json.append(svm.serialize)

        #return JsonResponse(svm_json, safe=False)
        serialized_rels = SVM.serialize_collection

    return JsonResponse(serialized_rels, safe=False)


@csrf_exempt
def create(request):
    if request.method == 'POST':
        f_bool = forms.BooleanField()  # A cool way to check fields and clean them, without doing much logic or switch case!
        svm_json = json.loads(request.body.decode('utf-8'))
        name = svm_json['name'].lower()
        is_active = f_bool.clean(svm_json['isActive'])
        response = {"error": "Could not save node"}
        svm = SVM(name=name, is_active=is_active)

        try:
            svm = SVM(name=name, is_active=is_active)
            svm.save()
            response = {"id": svm.id}

        except:
            print("could not save svm: ")
            print(svm.serialize)

        return JsonResponse(response)

    return JsonResponse('not from get_all_node', safe=False)
