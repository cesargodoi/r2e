from django.shortcuts import render


def tools(request):
    return render(request, "base/tools.html", context={"title": "Tools"})
