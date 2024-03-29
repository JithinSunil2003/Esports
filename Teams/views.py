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
    return render(request,"Teams/Homepage.html")


def Myprofile (request):
  if "teamid" in request.session:
    team = db.collection("tbl_teamreg").document(request.session["teamid"]).get().to_dict()
    return render(request,"Teams/Myprofile.html",{"team":team})
  else:
    return render(request,"Guest/Login.html")


def Editprofile(request):
  team = db.collection("tbl_teamreg").document(request.session["teamid"]).get().to_dict()
  if request.method=="POST":
    data={"team_name":request.POST.get("name"),"team_contact":request.POST.get("contact"),"team_address":request.POST.get("address")}
    db.collection("tbl_teamreg").document(request.session["teamid"]).update(data)
    return redirect("webteams:Myprofile")
  else:
    return render(request,"Teams/EditProfile.html",{"team":team})  


def changepassword(request):
  organizer = db.collection("tbl_teamreg").document(request.session["teamid"]).get().to_dict()
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
  if "teamid" in request.session:
    com=db.collection("tbl_complaint").where("team_id","==",request.session["teamid"]).stream()
    com_data=[]
    for i in com:
        data=i.to_dict()
        com_data.append({"com":data,"id":i.id})
    if request.method=="POST":
        datedata = date.today()
        data={"user_id":0,"organizer_id":0,"complaint_content":request.POST.get("content"),"team_id":request.session["teamid"],"complaint_status":0,"complaint_date":str(datedata)}
        db.collection("tbl_complaint").add(data)
        return redirect("webteams:complaint")
    else:
      return render(request,"Teams/Complaint.html",{"com":com_data})
  else:
    return render(request,"Guest/Login.html")

def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("webteams:complaint")  

def feedback(request):
  if "teamid" in request.session:
    feed=db.collection("tbl_feedback").where("team_id","==",request.session["teamid"]).stream()
    feed_data=[]
    for i in feed:
        data=i.to_dict
        feed_data.append({"feed":data,"id":i.id})
    if request.method=="POST":
      data={"feedback_content":request.POST.get("content"),"team_id":request.session["teamid"]}
      db.collection("tbl_feedback").add(data)
      return redirect("webteams:feedback")
    else:
      return render(request,"Teams/Feedback.html",{"feed":feed_data})  
  else:
    return render(request,"Guest/Login.html")

def delfeedback(request,id):
  db.collection("tbl_feedback").document(id).delete()
  return redirect("webteams:feedback")    


def achivements(request):
  if "teamid" in request.session:
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
  else:
    return render(request,"Guest/Login.html")


def delachivements(request,id):
  db.collection("tbl_achivements"),document(id).delete()
  return redirect("webteams:achivements")


def members(request):
  if "teamid" in request.session:
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
  else:
    return render(request,"Guest/Login.html")


def delmembers(request,id):
  db.collection("tbl_teammember").document(id).delete()
  return redirect("webteams:members") 


def viewevent(request):
  if "teamid" in request.session:
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
    return render(request,"Teams/ViewEvents.html",{"event_data":result})
  else:
    return render(request,"Guest/Login.html")

def Req(request,id):
  if "teamid" in request.session:
    req=db.collection("tbl_request").where("team_id","==",request.session["teamid"]).stream()
    req_data=[]
    datedata = date.today() 
    data={"organizer_id":request.session["oid"],"event_id":id,"team_id":request.session["teamid"],"request_status":0,"request_date":str(datedata)}
    db.collection("tbl_request").add(data)
    event = db.collection("tbl_event").document(id).get().to_dict()
    count = int(event["event_count"])
    if count == 0:
      return render(request,"Teams/ViewEvents.html",{"msg":"No slot Avalible"})
    else:
      bal = count - 1
      db.collection("tbl_event").document(id).update({"event_count":bal})
    return redirect("webteams:viewevent")
  else:
    return render(request,"Guest/Login.html")


def viewreq(request):
  if "teamid" in request.session:
    req=db.collection("tbl_request").where("team_id", "==", request.session["teamid"]).stream()
    req_data=[]
    for i in req:
      data=i.to_dict()
      event = db.collection("tbl_event").document(data["event_id"]).get().to_dict()
      req_data.append({"view":data,"id":i.id,"event":event})
    return render(request,"Teams/ViewRequest.html",{"view":req_data})
  else:
    return render(request,"Guest/Login.html")

def viewmemreq(request):
  if "teamid" in request.session:
    memreq=db.collection("tbl_memberreq").where("member_request_status","==",0).stream()
    memreq_data=[]

    for i in memreq:
      data=i.to_dict()
      user=db.collection("tbl_userreg").document(data["user_id"]).get().to_dict()
      memreq_data.append({"view":data,"id":i.id,"user":user})
    return render(request,"Teams/MemberRequest.html",{"view":memreq_data})
  else:
    return render(request,"Guest/Login.html")


def accept(request,id):
  req=db.collection("tbl_memberreq").document(id).update({"member_request_status":1})
  req = db.collection("tbl_memberreq").document(id).get().to_dict()
  user = db.collection("tbl_userreg").document(req["user_id"]).get().to_dict()
  email = user["user_email"]
  send_mail(
          'Member ', #subject
          "\rHello \r\nYour Request Has Been Accepted. " + email +" Welcome to the team ." ,#body
          settings.EMAIL_HOST_USER,
          [email],
    )
  return redirect("webteams:viewmemreq")  


def reject(request,id):
  req=db.collection("tbl_memberreq").document(id).update({"member_request_status":2})
  req = db.collection("tbl_memberreq").document(id).get().to_dict()
  user = db.collection("tbl_userreg").document(req["user_id"]).get().to_dict()
  email = user["user_email"]
  send_mail(
          'Member ', #subject
          "\rHello \r\nYour Request Has Been Rejected. " + email  ,#body
          settings.EMAIL_HOST_USER,
          [email],
    )
  return redirect("webteams:viewmemreq")  


  return redirect("webteams:viewmemreq") 

def accepted(request):
  if "teamid" in request.session:
    memreq=db.collection("tbl_memberreq").where("member_request_status","==",1).stream()
    memreq_data=[]
    for i in memreq:
      data=i.to_dict()
      user=db.collection("tbl_userreg").document(data["user_id"]).get().to_dict()
      memreq_data.append({"view":data,"id":i.id,"user":user})
    return render(request,"Teams/Accepted.html",{"view":memreq_data})
  else:
    return render(request,"Guest/Login.html")
  

def rejected(request):
  if "teamid" in request.session:
    memreq=db.collection("tbl_memberreq").where("request_status","==",2).stream()
    memreq_data=[]
    for i in memreq:
      data=i.to_dict()
      user=db.collection("tbl_userreg").document(data["user_id"]).get().to_dict()
      memreq_data.append({"view":data,"id":i.id,"user":user})
    return render(request,"Teams/Rejected.html",{"view":memreq_data})
  else:
    return render(request,"Guest/Login.html")
def chat(request,id):
  if "teamid" in request.session:
    to_user = db.collection("tbl_user").document(id).get().to_dict()
    return render(request,"Teams/Chat.html",{"user":to_user,"tid":id})
  else:
    return render(request,"Guest/Login.html")  

def ajaxchat(request):
    image = request.FILES.get("file")
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        st.child(path).put(image)
        d_url = st.child(path).get_url(None)
        db.collection("tbl_chat").add({"chat_content":"","chat_time":datetime.now(),"team_from":request.session["teamid"],"user_to":request.POST.get("tid"),"chat_file":d_url,"user_from":"","team_to":""})
        return render(request,"Teams/Chat.html",{"tid":tid})
    else:
      if request.POST.get("msg"):
        db.collection("tbl_chat").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"team_from":request.session["teamid"],"user_to":request.POST.get("tid"),"chat_file":"","user_from":"","team_to":""})
        return render(request,"Teams/Chat.html",{"tid":tid})
      else:
        return render(request,"Teams/Chat.html",{"tid":tid})


def ajaxchatview(request):
    tid = request.GET.get("tid")
    user_ref = db.collection("tbl_chat")
    chat = db.collection("tbl_chat").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["team_from"] == request.session["teamid"]) | (cdata["team_to"] == request.session["teamid"])) & ((cdata["user_from"] == tid) | (cdata["user_to"] == tid)):
            data.append(cdata)
    return render(request,"Teams/ChatView.html",{"data":data,"tid":tid})

def clearchat(request):
  if "teamid" in request.session:
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat").where("team_from", "==", request.session["teamid"]).where("user_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat").where("team_to", "==", request.session["teamid"]).where("user_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"Teams/ClearChat.html",{"msg":"Chat Cleared Sucessfully....."})
  else:
    return render(request,"Guest/Login.html")
#################################################################################################################################

def chat2(request,id):
  if "teamid" in request.session:
    to_org = db.collection("tbl_orgreg").document(id).get().to_dict()
    return render(request,"Teams/Chat2.html",{"user":to_org,"tid":id})
  else:
    return render(request,"Guest/Login.html")  

def ajaxchat2(request):
    image = request.FILES.get("file")
    print(image)
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        st.child(path).put(image)
        d_url = st.child(path).get_url(None)
        db.collection("tbl_chat2").add({"chat_content":"","chat_time":datetime.now(),"team_from":request.session["teamid"],"org_to":request.POST.get("tid"),"chat_file":d_url,"team_to":"","org_from":""})
        return render(request,"Teams/Chat2.html",{"tid":tid})
    else:
      if request.POST.get("msg"):
        db.collection("tbl_chat2").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"team_from":request.session["teamid"],"org_to":request.POST.get("tid"),"chat_file":"","team_to":"","org_from":""})
        return render(request,"Teams/Chat2.html",{"tid":tid})
      else:
        return render(request,"Teams/Chat2.html",{"tid":tid})

def ajaxchatview2(request):
    tid = request.GET.get("tid")
    chat = db.collection("tbl_chat2").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["team_from"] == request.session["teamid"]) | (cdata["team_to"] == request.session["teamid"])) & ((cdata["org_from"] == tid) | (cdata["org_to"] == tid)):
            data.append(cdata)
    return render(request,"Teams/ChatView2.html",{"data":data,"tid":tid})

def clearchat2(request):
  if "teamid" in request.session:
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat2").where("team_from", "==", request.session["teamid"]).where("org_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat2").where("team_to", "==", request.session["teamid"]).where("org_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"Teams/ClearChat2.html",{"msg":"Chat Cleared Sucessfully....."})
  else:
    return render(request,"Guest/Login.html")


def payment(request,id):
  if "teamid" in request.session:
    req = db.collection("tbl_request").document(id).get().to_dict()
    event = db.collection("tbl_event").document(req["event_id"]).get().to_dict()
    tot = event["event_amount"]
    if request.method == "POST":
      db.collection("tbl_request").document(id).update({"request_status":3})
      return redirect("webteams:loader")
    else:
      return render(request,"Teams/Payment.html",{"total":tot})
  else:
    return render(request,"Guest/Login.html")

def loader(request):
  return render(request,"Teams/Loader.html")

def paymentsuc(request):
  return render(request,"Teams/Payment_suc.html")


def viewreply(request):
    if 'teamid' in request.session:
        com = db.collection("tbl_complaint").where("team_id", "==", request.session["teamid"]).stream()
        com_data = []
        for c in com:
            com_data.append({"complaint":c.to_dict(),"id":c.id})
        return render(request,"Teams/ViewReply.html",{"com":com_data})
    else:
        return redirect("webguest:login")


def logout(request):
    del request.session["teamid"]
    return redirect("webguest:login")           