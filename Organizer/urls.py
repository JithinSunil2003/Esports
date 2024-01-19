from django.urls import path
from Organizer import views
app_name="weborganizer"

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('Myprofile/',views.Myprofile,name="Myprofile"),
    path('Editprofile/',views.Editprofile,name="Editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('Event/',views.event,name="event"),  
   path('editevent/<str:id>',views.editevent,name="editevent"),
    
]