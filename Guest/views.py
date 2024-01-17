from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase


db=firestore.client()

# Create your views here.

def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id", "==", request.GET.get("did")).stream()
    place_data = []
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})


def orgreg(request):
    return render(request,"Guest/Organizer.html")