from django.shortcuts import render
def home_view(request):
    return render(request, "main.html")


def permission_denied_view(request, exception=None):
    return render(request, "main/no-access", status=403)
