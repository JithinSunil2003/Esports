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
    return render(request,"Teams/Homepage.html")


def Myprofile (request):
    team = db.collection("tbl_teamreg").document(request.session["tid"]).get().to_dict()
    return render(request,"Teams/Myprofile.html",{"team":team})

def Editprofile(request):
  team = db.collection("tbl_teamreg").document(request.session["tid"]).get().to_dict()
  if request.method=="POST":
    data={"team_name":request.POST.get("name"),"team_contact":request.POST.get("contact"),"team_address":request.POST.get("address")}
    db.collection("tbl_teamreg").document(request.session["tid"]).update(data)
    return redirect("webteams:Myprofile")
  else:
    return render(request,"Teams/EditProfile.html",{"team":team})  


def changepassword(request):
  organizer = db.collection("tbl_teamreg").document(request.session["tid"]).get().to_dict()
  email = organizer["team_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
    settings.EMAIL_HOST_USER,
    [email],
  )
  return render(request,"Teams/Homepage.html",{"msg":email})