from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date,datetime


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
  if "uid" in request.session:
    user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
    return render(request,"User/Myprofile.html",{"user":user})
  else:
    return render(request,"Guest/Login.html")

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
  if "uid" in request.session:
    com=db.collection("tbl_complaint").where("user_id","==",request.session["uid"]).stream()
    com_data=[]
    for i in com:
      data=i.to_dict()
      com_data.append({"com":data,"id":i.id})
    if request.method=="POST":
      datedata = date.today()
      data={"team_id":0,"complaint_content":request.POST.get("content"),"user_id":request.session["uid"],"complaint_status":0,"complaint_date":str(datedata)}
      db.collection("tbl_complaint").add(data)
      return redirect("webuser:complaint")
    else:
      return render(request,"User/Complaint.html",{"com":com_data})
  else:
    return render(request,"Guest/Login.html")    


def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("webuser:complaint")  

def feedback(request):
  if "uid" in request.session:
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
  else:
    return render(request,"Guest/Login.html")

def delfeedback(request,id):
  db.collection("tbl_feedback").document(id).delete()
  return redirect("webuser:feedback")    


def viewteams(request):
  if "uid" in request.session:
    team=db.collection("tbl_teamreg").stream()
    team_data=[]
    for i in team:
      data=i.to_dict
      team_data.append({"team":data,"id":i.id})
    return render(request,"User/ViewTeams.html",{"team":team_data})
  else:
    return render(request,"Guest/Login.html")

def memberreq(request,id):
  if "uid" in request.session:
    team=db.collection("tbl_teamreg").where("user_id","==",request.session["uid"]).stream()
    team_data=[]
    datedata = date.today()
    data={"team_id":request.session["teamid"],"member_request_status":0,"user_id":request.session["uid"],"member_request_date":str(datedata)}
    db.collection("tbl_memberreq").add(data)
    return redirect("webuser:viewteams")
  else:
    return render(request,"Guest/Login.html")

def myreq(request):
  if "uid" in request.session:
    memreq=db.collection("tbl_memberreq").where("user_id","==",request.session["uid"]).stream()
    memreq_data=[]
    for i in memreq:
      data=i.to_dict()
      team=db.collection("tbl_teamreg").document(data["team_id"]).get().to_dict()
      memreq_data.append({"view":data,"id":i.id,"team":team})
    return render(request,"User/MyRequest.html",{"view":memreq_data})
  else:
    return render(request,"Guest/Login.html")  


def myteam(request):
  if "uid" in request.session:
    memreq=db.collection("tbl_memberreq").where("user_id","==",request.session["uid"]).stream()
    memreq_data=[]
    for i in memreq:
      data=i.to_dict()
      team=db.collection("tbl_teamreg").document(data["team_id"]).get().to_dict()
      memreq_data.append({"view":data,"id":i.id,"team":team})
    return render(request,"User/MyTeam.html",{"view":memreq_data})
  else:
    return render(request,"Guest/Login.html")      
  
def chat(request,id):
  if "uid" in request.session:
    to_team = db.collection("tbl_teamreg").document(id).get().to_dict()
    return render(request,"User/Chat.html",{"user":to_team,"tid":id})
  else:
    return render(request,"Guest/Login.html")  

def ajaxchat(request):
    image = request.FILES.get("file")
    print(image)
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        st.child(path).put(image)
        d_url = st.child(path).get_url(None)
        db.collection("tbl_chat").add({"chat_content":"","chat_time":datetime.now(),"user_from":request.session["uid"],"team_to":request.POST.get("tid"),"chat_file":d_url,"team_from":"","user_to":""})
        return render(request,"User/Chat.html",{"tid":tid})
    else:
      if request.POST.get("msg"):
        db.collection("tbl_chat").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"user_from":request.session["uid"],"team_to":request.POST.get("tid"),"chat_file":"","team_from":"","user_to":""})
        return render(request,"User/Chat.html",{"tid":tid})
      else:
        return render(request,"User/Chat.html",{"tid":tid})


def ajaxchatview(request):
    tid = request.GET.get("tid")
    user_ref = db.collection("tbl_chat")
    chat = db.collection("tbl_chat").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["user_from"] == request.session["uid"]) | (cdata["user_to"] == request.session["uid"])) & ((cdata["team_from"] == tid) | (cdata["team_to"] == tid)):
            data.append(cdata)
    return render(request,"User/ChatView.html",{"data":data,"tid":tid})

def clearchat(request):
  if "uid" in request.session:
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat").where("user_from", "==", request.session["uid"]).where("team_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat").where("user_to", "==", request.session["uid"]).where("team_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"User/ClearChat.html",{"msg":"Chat Cleared Sucessfully....."})
  else:
    return render(request,"Guest.html")  


def viewreply(request):
    if 'uid' in request.session:
        com = db.collection("tbl_complaint").where("user_id", "==", request.session["uid"]).stream()
        com_data = []
        for c in com:
            com_data.append({"complaint":c.to_dict(),"id":c.id})
        return render(request,"User/ViewReply.html",{"com":com_data})
    else:
        return redirect("webguest:login")    


def logout(request):
    del request.session["uid"]
    return redirect("webguest:login")   


def viewevent(request):
  if "uid" in request.session:
    Etype=db.collection("tbl_Eventtype").where("team_id","==",request.session["teamid"]).stream()
    Etype_data=[]
    for i in Etype:
      data=i.to_dict()
      Etype_data.append({"Etype":i.to_dict(),"id":i.id})
    result=[]
    event_data=db.collection("tbl_event").stream()
    for event in event_data:
      event_dict=event.to_dict()
      Etype=db.collection("tbl_Eventtype").document(event_dict["Eventtype_id"]).get().to_dict()
      result.append({'Etypedata':Etype,'event_data':event_dict,'eventid':event.id})
    return render(request,"User/ViewEvents.html",{"event_data":result})
  else:
    return render(request,"Guest/Login.html")   