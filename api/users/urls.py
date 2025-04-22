from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.users.views import UserListCreateView, RegisterView, LoginView

router = SimpleRouter()
router.register(r'users', UserListCreateView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/register/', RegisterView.as_view(), name='register'),
    path('v1/login/', LoginView.as_view(), name='login')

]
