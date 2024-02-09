from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date


db=firestore.client()

config = {
  "apiKey": "AIzaSyDVNLi8RAAcmPeKJlQXf0e4YsEzrp4F7Cs",
  "authDomain": "esports-80872.firebaseapp.com",
  "projecuid": "esports-80872",
  "storageBucket": "esports-80872.appspot.com",
  "messagingSenderId": "611016670354",
  "appId": "1:611016670354:web:db3c9b9ca29dc66505ba4b",
  "measuremenuid": "G-32X3NGQWCJ",
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()



# Create your views here.
def homepage(request):
    return render(request,"user/Homepage.html")


def Myprofile (request):
    user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
    return render(request,"User/Myprofile.html",{"user":user})

def Editprofile(request):
  user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
  if request.method=="POST":
    data={"user_name":request.POST.get("name"),"user_contact":request.POST.get("contact"),"user_address":request.POST.get("address")}
    db.collection("tbl_userreg").document(request.session["uid"]).update(data)
    return redirect("webuser:Myprofile")
  else:
    return render(request,"User/EditProfile.html",{"user":user})  


def changepassword(request):
  user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
  email = user["user_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET user.",#body
    settings.EMAIL_HOST_user,
    [email],
  )
  return render(request,"User/Homepage.html",{"msg":email})

def complaint(request):
  com=db.collection("tbl_complaint").where("user_id","==",request.session["uid"]).stream()
  com_data=[]
  for i in com:
    data=i.to_dict()
    com_data.append({"com":data,"id":i.id})
  if request.method=="POST":
    datedata = date.today()
    data={"complaint_content":request.POST.get("content"),"user_id":request.session["uid"],"complaint_status":0,"complaint_date":str(datedata)}
    db.collection("tbl_complaint").add(data)
    return redirect("webuser:complaint")
  else:
    return render(request,"User/Complaint.html",{"com":com_data})


def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("webuser:complaint")  

def feedback(request):
  feed=db.collection("tbl_feedback").where("user_id","==",request.session["uid"]).stream()
  feed_data=[]
  for i in feed:
    data=i.to_dict
    feed_data.append({"feed":data,"id":i.id})
  if request.method=="POST":
    data={"feedback_content":request.POST.get("content"),"user_id":request.session["uid"]}
    db.collection("tbl_feedback").add(data)
    return redirect("webuser:feedback")
  else:
    return render(request,"User/Feedback.html",{"feed":feed_data})  


def delfeedback(request,id):
  db.collection("tbl_feedback").document(id).delete()
  return redirect("webuser:feedback")    


def viewteams(request):
  
  return render(request,"User/ViewTeams.html")