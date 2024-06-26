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
    path('delevent/<str:id>',views.delevent,name="delevent"),
    path('Complaint/',views.complaint,name="complaint"),
    path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
    path('Feedback/',views.feedback,name="feedback"),
    path('delfeedback/<str:id>',views.delfeedback,name="delfeedback"),
    path('viewreq/',views.viewreq,name="viewreq"),
    path('accepted/<str:id>',views.accepted,name="accepted"),
    path('rejected/<str:id>',views.rejected,name="rejected"),
    path('acceptedlist/<str:id>',views.acceptedlist,name="acceptedlist"),
    path('rejectedlist/',views.rejectedlist,name="rejectedlist"),
    path('compl/',views.rejectedlist,name="rejectedlist"),
    path('schedule/',views.schedule,name="schedule"),
    path('viewreply/',views.viewreply,name="viewreply"),
    path('schedule_matches/',views.schedule_matches,name="schedule_matches"),
    path('view_matches/',views.view_matches,name="view_matches"),
    path('compelted/',views.compelted,name="compelted"),

    path('chat/<str:id>',views.chat,name="chat"),
    path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
    path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
    path('clearchat/',views.clearchat,name="clearchat"),
    path('logout/',views.logout,name="logout"),
]