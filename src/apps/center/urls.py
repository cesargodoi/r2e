from django.urls import path
from . import views

app_name = "center"

urlpatterns = [
    path("", views.CenterList.as_view(), name="list"),
    path("create/", views.CenterCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.CenterUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.CenterDelete.as_view(), name="delete"),
    path("search/", views.CenterSearch.as_view(), name="search"),
]
