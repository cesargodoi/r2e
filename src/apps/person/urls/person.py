from django.urls import path

from .. import views

app_name = "person"

urlpatterns = [
    path("", views.PersonList.as_view(), name="list"),
    path("create/", views.PersonCreate.as_view(), name="create"),
    path("check_name/", views.check_name, name="check_name"),
    path("<int:pk>/detail/", views.PersonDetail.as_view(), name="detail"),
    path("<int:pk>/update/", views.PersonUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.PersonDelete.as_view(), name="delete"),
    path(
        "<int:pk>/change-center/",
        views.ChangeCenter.as_view(),
        name="change_center",
    ),
]
