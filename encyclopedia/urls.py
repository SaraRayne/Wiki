from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit", views.edit, name="edit"),
    path("save_edits", views.save_edits, name="save_edits"),
    path("random_choice", views.random_choice, name="random_choice"),
    path("<str:title>", views.title, name="title")
]
