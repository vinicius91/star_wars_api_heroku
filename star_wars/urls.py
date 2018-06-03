from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('star_wars_api.urls')),
]
