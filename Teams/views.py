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

def complaint(request):
  if 'tid' in request.session:
    com=db.collection("tbl_complaint").where("team_id","==",request.session["tid"]).stream()
    com_data=[]
  for i in com:
      data=i.to_dict()
      com_data.append({"com":data,"id":i.id})
  if request.method=="POST":
      datedata = date.today()
      data={"complaint_content":request.POST.get("content"),"team_id":request.session["tid"],"complaint_status":0,"complaint_date":str(datedata)}
      db.collection("tbl_complaint").add(data)
      return redirect("webteams:complaint")
  else:
    return render(request,"Teams/Complaint.html",{"com":com_data})


def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("webteams:complaint")  

def feedback(request):
  feed=db.collection("tbl_feedback").where("team_id","==",request.session["tid"]).stream()
  feed_data=[]
  for i in feed:
      data=i.to_dict
      feed_data.append({"feed":data,"id":i.id})
  if request.method=="POST":
    data={"feedback_content":request.POST.get("content"),"team_id":request.session["tid"]}
    db.collection("tbl_feedback").add(data)
    return redirect("webteams:feedback")
  else:
    return render(request,"Teams/Feedback.html",{"feed":feed_data})  


def delfeedback(request,id):
  db.collection("tbl_feedback").document(id).delete()
  return redirect("webteams:feedback")    


def achivements(request):
  achive=db.collection("tbl_achivements").stream()
  achive_data=[]
  for i in achive:
    data=i.to_dict
    achive_data.append({"achive":data,"id":i.id})
  if request.method=="POST":
    image = request.FILES.get("Photo")
    if image:
      path = "AchivementsPhoto/" + image.name
      st.child(path).put(image)
      a_url = st.child(path).get_url(None)
     
    data={"achivements_name":request.POST.get("name"),"achivements_description":request.POST.get("description"),"achivements_photo":a_url}
    db.collection("tbl_achivements").add(data)
    return redirect("webteams:achivements")
  else:
    return render(request,"Teams/achivements.html",{"achivements":achive_data})  


def delachivements(request,id):
  db.collection("tbl_achivements"),document(id).delete()
  return redirect("webteams:achivements")


def members(request):
  members=db.collection("tbl_teammember").stream()
  member_data=[]
  for i in members:
    data=i.to_dict
    member_data.append({'members':data,"id":i.id})
  if request.method=="POST":
    data={"member_name":request.POST.get("name"),"member_contact":request.POST.get("contact"),"member_email":request.POST.get("email"),"member_address":request.POST.get("address")}
    db.collection("tbl_teammember").add(data)
    return redirect("webteams:members")  
  else:  
    return render(request,"Teams/TeamMembers.html",{"members":member_data})

def delmembers(request,id):
  db.collection("tbl_teammember").document(id).delete()
  return redirect("webteams:members") 

