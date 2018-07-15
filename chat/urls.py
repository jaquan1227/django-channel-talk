from django.conf.urls import url, include
from rest_framework import routers
from .views import *
from rest_framework_jwt.views import *
from .expire_checker import expire_checker
router = routers.DefaultRouter()

router.register(r'admin/users', UserAdminViewSet)
router.register(r'users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'msgs', MessageViewSet)

auth_urlpatterns = [
    url(r'^auth/register/', UserViewSet.as_view({"post":"create"})),
    url(r'^auth/login/', obtain_jwt_token),
    url(r'^auth/logout/', refresh_jwt_token),
    url(r'^auth/verify/', verify_jwt_token)    
]

chat_urlpatterns = [
    url(r'^chat/(?P<room_name>[^/]+)/$', room, name='room'),
]

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]

urlpatterns+= auth_urlpatterns
urlpatterns+= chat_urlpatterns

# after migrate , plz activate this line
# expire_checker(100,repeat=10, repeat_until=None)