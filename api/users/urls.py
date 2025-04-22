from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.users.views import UserListCreateView

router = SimpleRouter()
router.register(r'users', UserListCreateView, basename='users')
urlpatterns = [
    path('', include(router.urls)),

]
