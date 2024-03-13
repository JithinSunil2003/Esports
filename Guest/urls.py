from django.urls import path
from Guest import views
app_name="webguest"

urlpatterns = [
    path('orgreg/',views.orgreg,name="orgreg"),
     path('userreg/',views.userreg,name="userreg"),
    path('teamreg/',views.teamreg,name="teamreg"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
    path('login/',views.login,name="login"),
    path('',views.index,name="index"),
    path('fpassword/',views.fpassword,name="fpassword"),
]