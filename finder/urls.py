from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("autocomplete/", views.autocomplete, name='autocomplete'),
    path("<str:subject_name>/", views.subject_view, name="subject"),
]
