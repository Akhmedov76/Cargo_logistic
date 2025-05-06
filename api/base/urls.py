from django.urls import path, include

urlpatterns = [
    path('admin-statistic/', include('api.order.urls')),
    path('chats/', include('api.chats.urls')),
]
