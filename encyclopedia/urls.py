from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("random", views.random, name="random")
]
