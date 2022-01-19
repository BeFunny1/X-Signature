from django.urls import path

from app.signature.views import Handler


urlpatterns = [
    path('signature', Handler.as_view(), name='signature'),
]
