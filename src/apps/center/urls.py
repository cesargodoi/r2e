from django.urls import path
from . import views

app_name = "center"

urlpatterns = [
    path("", views.CenterList.as_view(), name="list"),
    path("<int:pk>/detail/", views.CenterDetail.as_view(), name="detail"),
    path("create/", views.CenterCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.CenterUpdate.as_view(), name="update"),
]
