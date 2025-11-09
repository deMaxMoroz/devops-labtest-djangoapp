from django.urls import path
from .views import api_info, health, NotesView

urlpatterns = [
    path("api/", api_info, name="api"),
    path("health/", health, name="health"),
    path("notes/", NotesView.as_view(), name="notes"),
]
