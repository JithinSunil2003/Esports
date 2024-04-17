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
def district(request):
    if "aid" in request.session:
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
    else:
        return render(request,"Guest/Login.html")

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
    if "aid" in request.session:
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
    else:
        return render(request,"Guest/Login.html")

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
    if "aid" in request.session:
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
    else:
        return render(request,"Guest/Login.html")

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

def admin(request):
    if "aid" in request.session:
        if request.method =="POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                admin = firebase_admin.auth.create_user(email=email,password=password)
            except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
                return render(request,"Admin/Admin.html",{"msg":error})
            db.collection("tbl_admin").add({"admin_id":admin.uid,"admin_name":request.POST.get("name"),"admin_contact":request.POST.get("contact"),"admin_email":request.POST.get("email")})    
            return render(request,"Admin/Admin.html")
        else:
            return render(request,"Admin/Admin.html")
    else:
        return redirect(request,"Guest/Login.html")

def homepage(request):
    if "aid" in request.session:
        return render(request,"Admin/Homepage.html")
    else:
        return render(request,"Guest/Login.html")


def viewcomplaint(request):
    if "aid" in request.session:
        organizer_data=[]
        user_data=[]
        team_data=[]
        tcom = db.collection("tbl_complaint").where("team_id", "!=",0).where("complaint_status", "==", 0).stream()
        for i in tcom:
            tdata = i.to_dict()
            team = db.collection("tbl_teamreg").document(tdata["team_id"]).get().to_dict()
            team_data.append({"complaint":i.to_dict(),"id":i.id,"team":team})

        ucom=db.collection("tbl_complaint").where("user_id","!=",0).where("complaint_status","==",0).stream()
        for i in ucom:
            udata = i.to_dict()
            user = db.collection("tbl_userreg").document(udata["user_id"]).get().to_dict()
            user_data.append({"complaint":i.to_dict(),"id":i.id,"user":user}) 

        ocom=db.collection("tbl_complaint").where("organizer_id","!=",0).where("complaint_status","==",0).stream()
        for i in ocom:
            odata = i.to_dict()
            organizer = db.collection("tbl_orgreg").document(odata["organizer_id"]).get().to_dict()
            organizer_data.append({"complaint":i.to_dict(),"id":i.id,"organizer":organizer}) 
        return render(request,"Admin/ViewComplaints.html",{"team":team_data,"user":user_data,"organizer":organizer_data})    
    else:
        return render(request,"Guest/Login.html")

def reply(request,id):
    if "aid" in request.session:
        if request.method == "POST":
                db.collection("tbl_complaint").document(id).update({"complaint_reply":request.POST.get("reply"),"complaint_status":"1"})
                return render(request,"Admin/Reply.html",{"msg":"Reply Sended..."})
        return render(request,"Admin/Reply.html")    
    else:
        return render(request,"Guest/Login.html")



def viewfeedback(request):
    if "aid" in request.session:
        organizer_data=[]
        user_data=[]
        team_data=[]
        feed=db.collection("tbl_feedback").stream()
        tfeed = db.collection("tbl_feedback").where("team_id", "!=",0).stream()
        for i in tfeed:
            tdata = i.to_dict()
            team = db.collection("tbl_teamreg").document(tdata["team_id"]).get().to_dict()
            team_data.append({"feedback":i.to_dict(),"id":i.id,"team":team})

        ufeed=db.collection("tbl_feedback").where("user_id","!=",0).stream()
        for i in ufeed:
            udata = i.to_dict()
            user = db.collection("tbl_userreg").document(udata["user_id"]).get().to_dict()
            user_data.append({"feedback":i.to_dict(),"id":i.id,"user":user}) 

        ofeed=db.collection("tbl_feedback").where("organizer_id","!=",0).stream()
        for i in ofeed:
            odata = i.to_dict()
            organizer = db.collection("tbl_orgreg").document(odata["organizer_id"]).get().to_dict()
            organizer_data.append({"feedback":i.to_dict(),"id":i.id,"organizer":organizer}) 
        return render(request,"Admin/ViewFeedback.html",{"team":team_data,"user":user_data,"organizer":organizer_data}) 
    else:
        return render(request,"Guest/Login.html")

def logout(request):
    del request.session["aid"]
    return redirect("webguest:login")        



def viewreply(request):
    if "aid" in request.session:
        organizer_data=[]
        user_data=[]
        team_data=[]
        tcom = db.collection("tbl_complaint").where("team_id", "!=",0).where("complaint_status", "==", 1).stream()
        for i in tcom:
            tdata = i.to_dict()
            team = db.collection("tbl_teamreg").document(tdata["team_id"]).get().to_dict()
            team_data.append({"complaint":i.to_dict(),"id":i.id,"team":team})

        ucom=db.collection("tbl_complaint").where("user_id","!=",0).where("complaint_status","==","1").stream()
        for i in ucom:
            udata = i.to_dict()
            user = db.collection("tbl_userreg").document(udata["user_id"]).get().to_dict()
            user_data.append({"complaint":i.to_dict(),"id":i.id,"user":user}) 

        ocom=db.collection("tbl_complaint").where("organizer_id","!=",0).where("complaint_status","==",1).stream()
        for i in ocom:
            odata = i.to_dict()
            organizer = db.collection("tbl_orgreg").document(odata["organizer_id"]).get().to_dict()
            organizer_data.append({"complaint":i.to_dict(),"id":i.id,"organizer":organizer}) 
        return render(request,"Admin/ViewComplaints.html",{"team":team_data,"user":user_data,"organizer":organizer_data})    
    else:
        return render(request,"Guest/Login.html")    