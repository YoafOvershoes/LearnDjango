from svmService.views import SvmViews
from django.urls import path, include

urlpatterns = [
    path('', include([
        path('all', SvmViews.get_all_svm),
        path('create', SvmViews.create)
        # can add more functions from the view
    ])),
]

#
# from svmService.views import SvmViews
# from django.urls import path
#
# urlpatterns = [
#     path('all', SvmViews.get_all_svm),
# ]
