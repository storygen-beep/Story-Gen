from django.contrib import admin
from django.urls import path

from messaging.views import whatsapp_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("webhooks/whatsapp/", whatsapp_webhook, name="whatsapp-webhook"),
]
