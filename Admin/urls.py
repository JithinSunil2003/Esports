from django.urls import path
from Admin import views
app_name="webadmin"

urlpatterns = [
        path('District/',views.district,name="district"),
        path('editdistrict/<str:id>',views.editdistrict,name="editdistrict"),
        path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
        path('Place/',views.Place,name="Place"),
        path('delplace/<str:id>',views.delplace,name="delplace"),
        path('editplace/<str:id>',views.editplace,name="editplace"),
       
        path('Eventtype/',views.eventtype,name="eventtype"),
        path('deleventtype/<str:id>',views.deleventtype,name="deleventtype"),
        path('editeventtype/<str:id>',views.editeventtype,name="editeventtype"),
       
        path('Admin/',views.admin,name="admin"),
        path('Homepage/',views.homepage,name="homepage"),
        

]