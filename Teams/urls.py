from django.urls import path
from Teams import views
app_name="webteams"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
    path("Myprofile/",views.Myprofile,name="Myprofile"),
    path("Editprofile/",views.Editprofile,name="Editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path('Complaint/',views.complaint,name="complaint"),
    path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
    path('Feedback/',views.feedback,name="feedback"),
    path('delfeedback/<str:id>',views.delfeedback,name="delfeedback"),
    path('Acheviments/',views.achivements,name="achivements"),
    path('delachivements/<str:id>',views.delachivements,name="delachivements"),
    path('TeamMembers/',views.members,name="members"),
    path('delmembers/<str:id>',views.delmembers,name="delmembers"),
    path('ViewEvent/',views.viewevent,name="viewevent"),
    path('request/<str:id>',views.Req,name="Req"),
    path('viewrequest/',views.viewreq,name="viewreq"),
    path('viewmemreq/',views.viewmemreq,name="viewmemreq"),
]