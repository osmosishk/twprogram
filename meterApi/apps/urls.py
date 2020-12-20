from . import views
from rest_framework.routers import DefaultRouter
from django.urls import re_path

# 路由列表
urlpatterns = [
    #path(r'login/$', obtain_jwt_token)
]

router = DefaultRouter()
router.register('data', views.MeterDataViewSet)
router.register('check', views.ParamViewSet)
router.register('meter', views.MeterViewSet)
router.register('upload', views.FileViewSet)

urlpatterns += router.urls