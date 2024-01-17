from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase


db=firestore.client()

# Create your views here.
def district(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    if request.method=="POST":
        data={"district_name":request.POST.get("district")}
        db.collection("tbl_district").add(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"district":dis_data})
    

def editdistrict(request,id):
    dis=db.collection("tbl_district").document(id).get().to_dict()
    if request.method=="POST":
       data={"district_name":request.POST.get("district")}
       db.collection("tbl_district").document(id).update(data)
       return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"dis_data":dis})


def deldistrict(request,id):
    db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:district")


def Place(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    result=[]
    place_data=db.collection("tbl_place").stream()
    for place in place_data:
        place_dict=place.to_dict()
        district=db.collection("tbl_district").document(place_dict["district_id"]).get()
        district_dict=district.to_dict()
        result.append({'districtdata':district_dict,'place_data':place_dict,'placeid':place.id})
    if request.method=="POST":
        data={"place_name":request.POST.get("place"),"district_id":request.POST.get("district")}
        db.collection("tbl_place").add(data)
        return redirect("webadmin:Place")
    else:
        return render(request,"Admin/Place.html",{"district":dis_data,"place":result})


def delplace(request,id):
    db.collection("tbl_place").document(id).delete()
    return redirect("webadmin:Place")        

def editplace(request,id):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"dis":d.to_dict(),"id":d.id})
    place_data=db.collection("tbl_place").document(id).get().to_dict()
    if request.method=="POST":
       place_data={"place_name":request.POST.get("place"),"district_id":request.POST.get("district")}
       db.collection("tbl_place").document(id).update(place_data)
       return redirect("webadmin:Place")
    else:
        return render(request,"Admin/Place.html",{"place_data":place_data,"district":dis_data})
   
def eventtype(request):
    Etype=db.collection("tbl_Eventtype").stream()
    Etype_data=[]
    for i in Etype:
        data=i.to_dict()
        Etype_data.append({"Etype":data,"id":i.id})
    if request.method=="POST":
        data={"Event_type":request.POST.get("Etype")}
        db.collection("tbl_Eventtype").add(data)
        return redirect("webadmin:eventtype")
    else:
        return render(request,"Admin/Eventtype.html",{"Etype":Etype_data})


def deleventtype(request,id):
    db.collection("tbl_Eventtype").document(id).delete()
    return redirect("webadmin:eventtype")       



def editeventtype(request,id):
    Etype=db.collection("tbl_Eventtype").document(id).get().to_dict()
    if request.method=="POST":
       data={"Event_type":request.POST.get("Etype")}
       db.collection("tbl_Eventtype").document(id).update(data)
       return redirect("webadmin:eventtype")
    else:
        return render(request,"Admin/Eventtype.html",{"Etype_data":Etype})




def event(request):
    Etype=db.collection("tbl_Eventtype").stream()
    Etype_data=[]
    for i in Etype:
        data=i.to_dict()
        Etype_data.append({"Etype":i.to_dict(),"id":i.id})
    result=[]
    event_data=db.collection("tbl_event").stream()
    for event in event_data:
        event_dict=event.to_dict()
        Etype=db.collection("tbl_Eventtype").document(Etype_dict["Eventtype_id"]).get()
        Etype_dict=Etype.to_dict()
        result.append({'Etypedata':Etype_dict,'event_data':event_dict,'eventid':event.id})
    if request.method=="POST":
        data={"event_name":request.POST.get("event"),"Eventtype_id":request.POST.get("etype")}
        db.collection("tbl_event").add(data)
        return redirect("webadmin:event")
    else:
        return render(request,"Admin/Event.html",{"Etype":Etype_data,"event":result})

    return render(request,"Admin/Event.html")

