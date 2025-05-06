from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet

router = DefaultRouter()

router.register(r'chats', ChatViewSet, basename='chats')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
