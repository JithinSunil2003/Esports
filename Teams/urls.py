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
    path('accept/<str:id>',views.accept,name="accept"),
    path('reject/<str:id>',views.reject,name="reject"),
    path('accepted/',views.accepted,name="accepted"),
    path('rejected/',views.rejected,name="rejected"),
    path('chat/<str:id>',views.chat,name="chat"),
    path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
    path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
    path('clearchat/',views.clearchat,name="clearchat"),

    path('chat2/<str:id>',views.chat2,name="chat2"),
    path('ajaxchat2/',views.ajaxchat2,name="ajaxchat2"),
    path('ajaxchatview2/',views.ajaxchatview2,name="ajaxchatview2"),
    path('clearchat2/',views.clearchat2,name="clearchat2"),

    path('payment/<str:id>',views.payment,name="payment"),
    path('loader/',views.loader,name="loader"),
    path('paymentsuc/',views.paymentsuc,name="paymentsuc"),
]