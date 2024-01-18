from django.urls import path
from Organizer import views
app_name="weborganizer"

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
]