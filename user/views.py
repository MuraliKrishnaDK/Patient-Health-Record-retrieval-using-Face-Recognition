from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import face_dataset
import main
import time
import Train
from firebase import firebase
firebase = firebase.FirebaseApplication('https://face-ae6b6-default-rtdb.firebaseio.com/', None)
n=""
update=0
e=""
def speak(mytext):
    # Import the required module for text 
    # to speech conversion
    from gtts import gTTS
      
    # This module is imported so that we can 
    # play the converted audio
    import os
      
    # The text that you want to convert to audio
    #mytext = 'Welcome to geeksforgeeks!'
      
    # Language in which you want to convert
    language = 'en'
      
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
      
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("welcome.mp3")
    from playsound import playsound
    playsound('welcome.mp3')
    os.remove('welcome.mp3')
    #pip install pygame
    # from pygame import mixer
    # import time
    # mixer.init() #Initialzing pyamge mixer
    
    # mixer.music.load('welcome.mp3') #Loading Music File
    
    # mixer.music.play() #Playing Music with Pygame
    # time.sleep()
    # mixer.music.stop()
    # Playing the converted file
    #os.system("mpg321 welcome.mp3")
##################################################################
####################index#######################################
def index(request):
    
    return render(request, 'user/index.html', {'title':'homepage',"a":"--","b":"--","c":"--","d":"--","e":"--","f":"--","g":"--","h":"--","i":"--","j":"--","k":"--","l":"--","m":"--"})


def train(request):
    speak("Training started, please do not perform any other operation it you get train completion messege. it may take from 5 min to 1 hour depending on number of dataset")
    print("training in progress")
    Train.main2()
    speak("training Dataset completed")
    return render(request, 'user/rating.html', {'title':'homepage'})
    
def fetchdetails(request):#find patient details
    global data,e,update
    print("in fetchdetails")
    res=main.main()
    print("res is",res)
    #res="10"
    if res =="unknown":
            return render(request, 'user/index.html',{'title':'fetch details','messages':['Unknown person']})

    a = firebase.get("patientDetails",res+"/name")
    b = firebase.get("patientDetails",res+"/econtact")
    c = firebase.get("patientDetails",res+"/Adress")
    d = firebase.get("patientDetails",res+"/Mhistory")
    e = firebase.get("patientDetails",res+"/pid")
    f = firebase.get("patientDetails",res+"/pAge")
    g = firebase.get("patientDetails",res+"/pbloodgrp")
    h = firebase.get("patientDetails",res+"/cdh")
    i = firebase.get("patientDetails",res+"/sah")
    j = firebase.get("patientDetails",res+"/folowup")
    k = firebase.get("patientDetails",res+"/occupation")
    l = firebase.get("patientDetails",res+"/state")
    m = firebase.get("patientDetails",res+"/timestamp")
    print(a,b,c,d,e,f,g,h,i,j,k,l,m)
    
    data={"a":a,"b":b,"c":c,"d":d,"e":e,"f":f,"g":g,"h":h,"i":i,"j":j,"k":k,"l":l,"m":m}
    # #print('\a\a\a\a')
    # if c != "NONE":
    #     import winsound
    #     winsound.Beep(440, 2000)
    update=1
    return render(request, 'user/index.html',{'title':'fetch details',"a":a,"b":b,"c":c,"d":d,"e":e,"f":f,"g":g,"h":h,"i":i,"j":j,"k":k,"l":l,"m":m,"update":update})

def adddetails(request):#adding patient details
    print("in adddetails")
    return render(request, 'user/rating.html',{'title':'adddetails'})


def adddetails2(request):#updating patient details
    global e,update,data,n
    print("patient id is ",e)
    update1=1
    return render(request, 'user/rating.html',{'title':'index',"n":e,"update":update1})
   
def senddetails(request):
    global n,update,data,e
   # print("data is",data)
    print("in senddetails")
    name = request.GET["name"]
    print("patient name is",name)
    econtact = request.GET["econtact"]
    print("patient econtact is",econtact)
    Adress = request.GET["Adress"]
    print("Adress is",Adress)
    Mhistory = request.GET["Mhistory"]
    print("Mhistory is",Mhistory)
    pAge = request.GET["pAge"]
    pbloodgrp = request.GET["pbloodgrp"]
    cdh = request.GET["cdh"]
    sah = request.GET["sah"]
    folowup = request.GET["folowup"]
    occupation = request.GET["occupation"]
    state = request.GET["state"]
    
    
    import datetime

    x = datetime.datetime.now()

    print(x)

    timestamp = x
 
    
    patientids=firebase.get("","patientids")
    print("patientids is ",patientids)

    if update ==0:
        
        while True:
            import random
            n = random.randint(0,22)
            print(n)
            n=str(n)
            if n in patientids.keys():
                print("found random")
            else:
                break
        if pbloodgrp not in ("A+","A-","B+","B-","O+","O-","Ab+","AB-"):
            return render(request, 'user/rating.html',{'title':'index','messages':['Choose valid blood group from  (A+,A-,B+,B-,O+,O-,Ab+,AB-)']})
        #face_dataset.main(n)
        if (len(econtact)<10 )and (not econtact.isdigit()):
            return render(request, 'user/rating.html',{'title':'index','messages':['invalid econtact']})
        if name =="" or econtact =="" or Adress=="" or  Mhistory=="":
            return render(request, 'user/rating.html',{'title':'index','messages':["please fill all columns"]})
        face_dataset.main(n)
    else:
        print("update record no new id generated")
        print("patient id is", e)
        n=e
        if name=="":
            name=data["a"]
            print("blank",name)
        if econtact=="":
            econtact=data["b"]
            print("blank",econtact)
        if Adress=="":
            Adress=data["c"]
            print("blank",Adress)
        if Mhistory=="":
            Mhistory=data["d"]
            print("blank",Mhistory)
        if pAge=="":
            pAge=data["f"]
            print("blank",pAge)
        if pbloodgrp=="":
            pbloodgrp=data["g"]
            print("blank",pbloodgrp)
        
        if cdh=="":
            cdh=data["h"]
            print("blank",cdh)
            
        if sah=="":
            sah=data["i"]
            print("blank",sah)
            
        if folowup=="":
            folowup=data["j"]
            print("blank",folowup)
        if occupation=="":
            occupation=data["k"]
            print("blank",occupation)
        if state=="":
            state=data["l"]
            print("blank",state)
        
    n=str(n)
    print("n is ",n)
    a = firebase.put("patientDetails",n+"/name",name)
    b = firebase.put("patientDetails",n+"/econtact",econtact)
    c = firebase.put("patientDetails",n+"/Adress",Adress)
    d = firebase.put("patientDetails",n+"/Mhistory",Mhistory)
    e = firebase.put("patientDetails",n+"/pid",n)
    e = firebase.put("patientids",n,name)
    f = firebase.put("patientDetails",n+"/pAge",pAge)
    g = firebase.put("patientDetails",n+"/pbloodgrp",pbloodgrp)
    h = firebase.put("patientDetails",n+"/cdh",cdh)
    i = firebase.put("patientDetails",n+"/sah",sah)
    j = firebase.put("patientDetails",n+"/folowup",folowup)
    k = firebase.put("patientDetails",n+"/occupation",occupation)
    l = firebase.put("patientDetails",n+"/state",state)
    m = firebase.put("patientDetails",n+"/timestamp",timestamp)
    
    update=0
    
    # #print('\a\a\a\a')
    # if c != "NONE":
    #     import winsound
    #     winsound.Beep(440, 2000)
        
    return render(request, 'user/index.html',{'title':'SendDetails',"messages":["Patient Added Successfully"]})

########################################################################
########### register here #####################################



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
           
            username = request.POST.get('username')
            #########################mail####################################
            htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("error in sending mail")
            ##################################################################
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form,'title':'reqister here'})

###################################################################################
################login forms###################################################


    
def Login(request):
    if request.method == 'POST':

        #AuthenticationForm_can_also_be_used__

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request,user)
            
            return render(request, 'user/index.html', {'form':form,'title':'homepage',"a":"--","b":"--","c":"--","d":"--","e":"--","f":"--","g":"--","h":"--","i":"--","j":"--","k":"--","l":"--","m":"--"})
            #return redirect('index',{"cnt":cnt})
        else:
            messages.info(request, f'account does not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form,'title':'log in'})
