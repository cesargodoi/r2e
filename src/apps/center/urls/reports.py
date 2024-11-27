from django.urls import path

from .. import views
from .center import urlpatterns

urlpatterns += [
    path(
        "reports/annual-frequency/",
        views.annual_frequency,
        name="reports__annual_frequency",
    ),
]
