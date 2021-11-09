from django.urls import path, include, re_path
from svmService.urls import SvmUrls

# from svmService import views

urlpatterns = [
    path('svm/', include(SvmUrls.urlpatterns))
]
