# Django_RouteView
Implement an auto-registered view


## Usage

Declare your view
```py
# views.py

from django_routeview import RouteView

class MyView(RouteView):

    route = "/myurl"
    name = "myname" # default to __name__

    def get(*args, **kwargs):
        pass
    ...
```

Import urls
```py
# urls.py

from django.urls import include

urlpatterns = [
    path("", include("django_routeview"))
]
```