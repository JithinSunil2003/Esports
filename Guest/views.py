from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase


db=firestore.client()

config = {
  "apiKey": "AIzaSyDVNLi8RAAcmPeKJlQXf0e4YsEzrp4F7Cs",
  "authDomain": "esports-80872.firebaseapp.com",
  "projectId": "esports-80872",
  "storageBucket": "esports-80872.appspot.com",
  "messagingSenderId": "611016670354",
  "appId": "1:611016670354:web:db3c9b9ca29dc66505ba4b",
  "measurementId": "G-32X3NGQWCJ",
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()

# Create your views here.

def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id", "==", request.GET.get("did")).stream()
    place_data = []
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})


def orgreg(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"dis":d.to_dict(),"id":d.id})
    if request.method =="POST":
        email = request.POST.get("orgemail")
        password = request.POST.get("password")
        try:
            org = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/Organizer.html",{"msg":error})
        image = request.FILES.get("orgphoto")
        if image:
            path = "OrgPhoto/" + image.name
            st.child(path).put(image)
            d_url = st.child(path).get_url(None)
        proof=request.FILES.get("orgproof")    
        if proof:
            path = "OrgProof/" + proof.name
            st.child(path).put(proof)
            p_url = st.child(path).get_url(None)     
        db.collection("tbl_orgreg").add({"org_id":org.uid,"org_name":request.POST.get("orgname"),"org_contact":request.POST.get("orgcontact"),"org_email":request.POST.get("orgemail"),"org_address":request.POST.get("orgaddress"),"place_id":request.POST.get("sel_place"),"org_photo":d_url,"org_proof":p_url})
        return render(request,"Guest/Organizer.html")
    else:
        return render(request,"Guest/Organizer.html",{"district":dis_data})

def login(request):
    organizer:""
    if request.method == "POST":
        email = request.POST.get("orgemail")
        password = request.POST.get("password")
        try:
            data = authe.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/Login.html",{"msg":"Error in Email Or Password"})
        organizer = db.collection("tbl_Organizer").where("organizer_id", "==", data["localId"]).stream()
        for u in organizer:
            organizerid = o.id
        if organizerid:
            request.session["oid"] = organizerid
            return redirect("weborganizer:homepage")    
    return render(request,"Guest/Login.html")    