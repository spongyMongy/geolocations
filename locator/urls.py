from django.urls import include, path
from rest_framework import routers
from . import views
from .views import LocalizationListApiView, SignUpView

router = routers.DefaultRouter()


urlpatterns = [
    # path('api-auth/', include('rest_framework.urls',
    #                           namespace='rest_framework')),
    path('', LocalizationListApiView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),

]