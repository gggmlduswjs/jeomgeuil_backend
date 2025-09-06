
from django.contrib import admin
from django.urls import path
from jeomgeuli_backend.core import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", v.health),
    path("api/learn/reset", v.learn_reset),
    path("api/learn/next", v.learn_next),
    path("api/chat/ask", v.chat_ask),
    path("api/braille/output", v.braille_output),
]
