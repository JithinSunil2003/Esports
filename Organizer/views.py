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
  if 'oid' in request.session:
    organizer = db.collection("tbl_orgreg").document(request.session["oid"]).get().to_dict()
    return render(request,"Organizer/Myprofile.html",{"organizer":organizer})
  else:
    return render(request,"Guest/Login.html")    

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
  if 'oid' in request.session:
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
      data={"organizer_id":request.session["oid"],"event_name":request.POST.get("ename"),"Eventtype_id":request.POST.get("etype"),"description":request.POST.get("description"),"event_count":request.POST.get("count"),"event_amount":request.POST.get("amount")}
      db.collection("tbl_event").add(data)
      return redirect("weborganizer:event")
    else:
      return render(request,"Organizer/Event.html",{"Etype":Etype_data,"event_data":result})
  else:
    return render(request,"Guest/Login.html")
   


def editevent(request,id):
    Etype = db.collection("tbl_Eventtype").stream()
    Etype_data = []
    for i in Etype:
        Etype_data.append({"Etype":i.to_dict(),"id":i.id})
    event_data=db.collection("tbl_event").document(id).get().to_dict()
    if request.method=="POST":
       event_data={"event_name":request.POST.get("ename"),"Eventtype_id":request.POST.get("etype"),"description":request.POST.get("description"),"event_count":request.POST.get("count"),"event_amount":request.POST.get("amount")}
       db.collection("tbl_event").document(id).update(event_data)
       return redirect("weborganizer:event")
    else:
        return render(request,"Organizer/Event.html",{"Etype":Etype_data,"eventdata":event_data})
     
def delevent(request,id):
    db.collection("tbl_event").document(id).delete()
    return redirect("weborganizer:event")       


def complaint(request):
  if 'oid' in request.session:
    com=db.collection("tbl_complaint").where("organizer_id","==",request.session["oid"]).stream()
    com_data=[]
    for i in com:
        data=i.to_dict()
        com_data.append({"com":data,"id":i.id})
    if request.method=="POST":
        datedata = date.today()
        data={"team_id":0,"user_id":0,"complaint_content":request.POST.get("content"),"organizer_id":request.session["oid"],"complaint_status":0,"complaint_date":str(datedata)}
        db.collection("tbl_complaint").add(data)
        return redirect("weborganizer:complaint")
    else:
      return render(request,"Organizer/Complaint.html",{"com":com_data})
  else:
    return render(request,"Guest/Login.html")

def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("weborganizer:complaint")  

def feedback(request):
  if 'oid' in request.session:
    feed=db.collection("tbl_feedback").where("organizer_id","==",request.session["oid"]).stream()
    feed_data=[]
    for i in feed:
        data=i.to_dict
        feed_data.append({"feed":data,"id":i.id})
    if request.method=="POST":
      
      data={"feedback_content":request.POST.get("content"),"organizer_id":request.session["oid"]}
      db.collection("tbl_feedback").add(data)
      return redirect("weborganizer:feedback")
    else:
      return render(request,"Organizer/Feedback.html",{"feed":feed_data})  
  else:
    return render(request,"Guest/Login.html")

def delfeedback(request,id):
  db.collection("tbl_feedback").document(id).delete()
  return redirect("weborganizer:feedback")    

def viewreq(request):
  if 'oid' in request.session:
    req=db.collection("tbl_request").where("request_status","==",0).stream()
    req_data=[]
    for i in req:
      data=i.to_dict()
      team = db.collection("tbl_teamreg").document(data["team_id"]).get().to_dict()
      req_data.append({"view":data,"id":i.id,"team":team})
    return render(request,"Organizer/ViewRequest.html",{"view":req_data})
  else:
    return render(request,"Guest/Login.html")

def accepted(request,id):
  req=db.collection("tbl_request").document(id).update({"request_status":1})
  return redirect("weborganizer:viewreq")

def rejected(request,id):
  req=db.collection("tbl_request").document(id).update({"request_status":2})
  return redirect("weborganizer:viewreq")  


def acceptedlist(request,id):
  if 'oid' in request.session:
    event = db.collection("tbl_event").document(id).get().to_dict()
    event_count = event["event_count"]
    req=db.collection("tbl_request").where("request_status","==",1).where("event_id","==",id).stream()
    req_data=[]
    for i in req:
      data=i.to_dict()
      team = db.collection("tbl_teamreg").document(data["team_id"]).get().to_dict()
      req_data.append({"accept":data,"id":i.id,"team":team})
    return render(request,"Organizer/AcceptedList.html",{"accept":req_data,"event_count":event_count})
  else:
    return render(request,"Guest/Login.html")

def rejectedlist(request):
  if 'oid' in request.session:
    req=db.collection("tbl_request").where("request_status","==",2).stream()
    req_data=[]
    for i in req:
      data=i.to_dict()
      team = db.collection("tbl_teamreg").document(data["team_id"]).get().to_dict()
      req_data.append({"reject":data,"id":i.id,"team":team})
    return render(request,"Organizer/RejectedList.html",{"reject":req_data})
  else:
    return render(request,"Guest/Login.html")  
  
def schedule(request):
  return render(request,"Organizer/Schedule.html")  

##Chat
def chat(request,id):
  if 'oid' in request.session:
      to_team = db.collection("tbl_teamreg").document(id).get().to_dict()
      return render(request,"Organizer/Chat.html",{"user":to_team,"tid":id})
  else:
    return render(request,"Guest/Login.html")

def ajaxchat(request):
    image = request.FILES.get("file")
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        st.child(path).put(image)
        d_url = st.child(path).get_url(None)
        db.collection("tbl_chat2").add({"chat_content":"","chat_time":datetime.now(),"org_from":request.session["oid"],"team_to":request.POST.get("tid"),"chat_file":d_url,"org_to":"","team_from":""})
        return render(request,"Organizer/Chat.html",{"tid":tid})
    else:
      if request.POST.get("msg"):
        db.collection("tbl_chat2").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"org_from":request.session["oid"],"team_to":request.POST.get("tid"),"chat_file":"","org_to":"","team_from":""})
        return render(request,"Organizer/Chat.html",{"tid":tid})
      else:
        return render(request,"Organizer/Chat.html",{"tid":tid})

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user_ref = db.collection("tbl_chat")
    chat = db.collection("tbl_chat2").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["org_from"] == request.session["oid"]) | (cdata["org_to"] == request.session["oid"])) & ((cdata["team_from"] == tid) | (cdata["team_to"] == tid)):
            data.append(cdata)
    return render(request,"Organizer/ChatView.html",{"data":data,"tid":tid})

def clearchat(request):
  if "oid" in session:
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat2").where("org_from", "==", request.session["oid"]).where("team_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat2").where("team_to", "==", request.session["oid"]).where("team_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"Organizer/ClearChat.html",{"msg":"Chat Cleared Sucessfully....."})
  else:
    return render(request,"Guest/Login.html")  


def viewreply(request):
    if 'oid' in request.session:
        com = db.collection("tbl_complaint").where("organizer_id", "==", request.session["oid"]).stream()
        com_data = []
        for c in com:
            com_data.append({"complaint":c.to_dict(),"id":c.id})
        return render(request,"Organizer/ViewReply.html",{"com":com_data})
    else:
        return redirect("webguest:login")        

def logout(request):
    del request.session["oid"]
    return redirect("webguest:login")           