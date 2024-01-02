from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "base/home.html", context={"title": "My Home"})


@login_required
def tools(request):
    return render(request, "base/tools.html", context={"title": "Tools"})


def permission_denied_403(request, exception):
    return render(request, "base/generics/403.html", status=403)
