from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path("arrival", views.arrival, name ="arrival"),
    path("api/<str:route>/<str:stopcode>", views.api, name="api")
]
