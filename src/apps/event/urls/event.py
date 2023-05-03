from django.urls import path
from .. import views

app_name = "event"

urlpatterns = [
    path("list/", views.EventList.as_view(), name="list"),
    path("<int:pk>/detail/", views.EventDetail.as_view(), name="detail"),
    path("create/", views.EventCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.EventUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.EventDelete.as_view(), name="delete"),
    # path("search/", views.EventSearch.as_view(), name="search"),
]
