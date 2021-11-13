from svmService.views import SvmViews
from django.urls import path, include

urlpatterns = [
    path('', include([
        path('all', SvmViews.get_all_svm),
        path('create', SvmViews.create),
        path('connect', SvmViews.connect_nodes_to_dr),
        # can add more functions from the view
    ])),
]
