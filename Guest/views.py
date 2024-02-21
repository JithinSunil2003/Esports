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

        
def teamreg(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"dis":d.to_dict(),"id":d.id})
    if request.method =="POST":
        email = request.POST.get("temail")
        password = request.POST.get("password")
        try:
            team = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/Teams.html",{"msg":error})
        image = request.FILES.get("tphoto")
        if image:
            path = "TeamPhoto/" + image.name
            st.child(path).put(image)
            t_url = st.child(path).get_url(None)
        proof=request.FILES.get("tproof")    
        if proof:
            path = "TeamProof/" + proof.name
            st.child(path).put(proof)
            e_url = st.child(path).get_url(None)     
        db.collection("tbl_teamreg").add({"team_id":team.uid,"team_name":request.POST.get("tname"),"team_contact":request.POST.get("tcontact"),"team_email":request.POST.get("temail"),"team_address":request.POST.get("taddress"),"place_id":request.POST.get("sel_place"),"team_photo":t_url,"team_proof":e_url})
        return render(request,"Guest/Teams.html")
    else:
        return render(request,"Guest/Teams.html",{"district":dis_data})


def userreg(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"dis":d.to_dict(),"id":d.id})
    if request.method =="POST":
        email = request.POST.get("uemail")
        password = request.POST.get("password")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/User.html",{"msg":error})
        image = request.FILES.get("uphoto")
        if image:
            path = "UserPhoto/" + image.name
            st.child(path).put(image)
            u_url = st.child(path).get_url(None)
         
        db.collection("tbl_userreg").add({"user_id":user.uid,"user_name":request.POST.get("uname"),"user_contact":request.POST.get("ucontact"),"user_email":request.POST.get("uemail"),"user_address":request.POST.get("uaddress"),"place_id":request.POST.get("sel_place"),"user_photo":u_url})
        return render(request,"Guest/User.html")
    else:
        return render(request,"Guest/user.html",{"district":dis_data})



def login(request):
    organizerid = ""
    teamid =""
    userid=""
    adminid=""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            data = authe.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/Login.html",{"msg":"Error in Email Or Password"})
        admin=db.collection("tbl_admin").where("admin_id","==",data["localId"]).stream() 
        for a in admin:
            adminid=a.id   
        organizer = db.collection("tbl_orgreg").where("org_id", "==", data["localId"]).stream()
        for o in organizer:
            organizerid = o.id
        team=db.collection("tbl_teamreg").where("team_id","==",data["localId"]).stream()    
        for t in team:
            teamid=t.id  
        user=db.collection("tbl_userreg").where("user_id","==",data["localId"]).stream()    
        for u in user:
            userid=u.id
        if organizerid:
            request.session["oid"] = organizerid
            return redirect("weborganizer:homepage")  
        elif teamid:
            request.session["teamid"]=teamid    
            return redirect("webteams:homepage")
        elif userid:
            request.session["uid"]=userid
            return redirect("webuser:homepage")   
        elif adminid:
            request.session["aid"]=adminid 
            return redirect("webadmin:homepage")  
        else:
            return render(request,"Guest/Login.html",{"msg":"error"})    
    else:
       return render(request,"Guest/Login.html")            