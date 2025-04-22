from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.users.views import UserListCreateView, RegisterView, LoginView

router = SimpleRouter()
router.register(r'users', UserListCreateView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login')

]
