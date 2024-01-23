from django.urls import path
from Teams import views
app_name="webteams"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
    path("Myprofile/",views.Myprofile,name="Myprofile"),
    path("Editprofile/",views.Editprofile,name="Editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path('Complaint',views.complaint,name="complaint"),
    path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
    path('Feedback/',views.feedback,name="feedback"),
    path('delfeedback/',views.delfeedback,name="delfeedback"),
    path('Acheviments/',views.Acheviments,name="Acheviments"),

]