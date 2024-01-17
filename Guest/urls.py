from django.urls import path
from Guest import views
app_name="webguest"

urlpatterns = [
    path('orgreg/',views.orgreg,name="orgreg"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
]