from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



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
def homepage(request):
    return render(request,"Organizer/Homepage.html")


def Myprofile (request):
    organizer = db.collection("tbl_orgreg").document(request.session["oid"]).get().to_dict()
    return render(request,"Organizer/Myprofile.html",{"organizer":organizer})

def Editprofile(request):
  organizer = db.collection("tbl_orgreg").document(request.session["oid"]).get().to_dict()
  if request.method=="POST":
    data={"org_name":request.POST.get("name"),"org_contact":request.POST.get("contact"),"org_address":request.POST.get("address")}
    db.collection("tbl_orgreg").document(request.session["oid"]).update(data)
    return redirect("weborganizer:Myprofile")
  else:
    return render(request,"Organizer/EditProfile.html",{"organizer":organizer})  

def changepassword(request):
  organizer = db.collection("tbl_orgreg").document(request.session["oid"]).get().to_dict()
  email = organizer["org_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
    settings.EMAIL_HOST_USER,
    [email],
  )
  return render(request,"Organizer/Homepage.html",{"msg":email})



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
        Etype=db.collection("tbl_Eventtype").document(event_dict["Eventtype_id"]).get()
        Etype_dict=Etype.to_dict()
        result.append({'Etypedata':Etype_dict,'event_data':event_dict,'eventid':event.id})
    if request.method=="POST":
        data={"event_name":request.POST.get("ename"),"Eventtype_id":request.POST.get("etype"),"description":request.POST.get("description")}
        db.collection("tbl_event").add(data)
        return redirect("weborganizer:event")
    else:
        return render(request,"Organizer/Event.html",{"Etype":Etype_data,"event_data":result})

    return render(request,"Organizer/Event.html")


def editevent(request,id):
    Etype = db.collection("tbl_Eventtype").stream()
    Etype_data = []
    for i in Etype:
        Etype_data.append({"Etype":i.to_dict(),"id":i.id})
    event_data=db.collection("tbl_event").document(id).get().to_dict()
    if request.method=="POST":
       event_data={"event_name":request.POST.get("ename"),"Eventtype_id":request.POST.get("etype"),"description":request.POST.get("description")}
       db.collection("tbl_event").document(id).update(event_data)
       return redirect("weborganizer:event")
    else:
        return render(request,"Organizer/Event.html",{"Etype":Etype_data,"eventdata":event_data})
     
def delevent(request,id):
    db.collection("tbl_event").document(id).delete()
    return redirect("weborganizer:event")       


def complaint(request):
  com=db.collection("tbl_complaint").stream()
  com_data=[]
  for i in com:
        data=i.to_dict()
        com_data.append({"com":data,"id":i.id})
  if request.method=="POST":
        data={"complaint_content":request.POST.get("content")}
        db.collection("tbl_complaint").add(data)
        return redirect("weborganizer:complaint")
  else:
        return render(request,"Organizer/Complaint.html",{"com":com_data})


def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("weborganizer:complaint")  

def feedback(request):
  feed=db.collection("tbl_feedback").stream()
  feed_data=[]
  for i in feed:
      data=i.to_dict
      feed_data.append({"feed":data,"id":i.id})
  if request.method=="POST":
    data={"feedback_content":request.POST.get("content")}
    db.collection("tbl_feedback").add(data)
    return redirect("weborganizer:feedback")
  else:
    return render(request,"Organizer/Feedback.html",{"feed":feed_data})  


def delfeedback(request,id):
  db.collection("tbl_feedback").document(id).delete()
  return redirect("weborganizer:feedback")    