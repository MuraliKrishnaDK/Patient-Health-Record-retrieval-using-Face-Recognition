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
import time
# Lazy imports to avoid TensorFlow loading during Django startup
# import face_dataset
# import main
# import Train

# Initialize Firebase connection
firebase = None
print("Firebase not available - using local fallback")

# Create a simple local database fallback
import json
import os

def get_local_data_file():
    return os.path.join(os.path.dirname(__file__), 'local_patient_data.json')

def load_local_data():
    data_file = get_local_data_file()
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except:
            return {"patientids": {}, "patientDetails": {}}
    return {"patientids": {}, "patientDetails": {}}

def save_local_data(data):
    data_file = get_local_data_file()
    try:
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False
n=""
update=0
e=""
data = {"a": "", "b": "", "c": "", "d": "", "e": "", "f": "", "g": "", "h": "", "i": "", "j": "", "k": "", "l": "", "m": ""}
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
    
    try:
        # For now, simulate face recognition with a test ID
        # In a real scenario, this would call the face recognition module
        res = "1"  # Simulate a recognized patient ID
        
        # Use local database to fetch patient details
        data = load_local_data()
        patient_details = data.get("patientDetails", {}).get(res, {})
        
        if not patient_details:
            return render(request, 'user/index.html',{'title':'fetch details','messages':['Patient not found in database']})

        a = patient_details.get("name", "")
        b = patient_details.get("econtact", "")
        c = patient_details.get("Adress", "")
        d = patient_details.get("Mhistory", "")
        e = patient_details.get("pid", "")
        f = patient_details.get("pAge", "")
        g = patient_details.get("pbloodgrp", "")
        h = patient_details.get("cdh", "")
        i = patient_details.get("sah", "")
        j = patient_details.get("folowup", "")
        k = patient_details.get("occupation", "")
        l = patient_details.get("state", "")
        m = patient_details.get("timestamp", "")
        
        print(f"Retrieved patient data: {a}, {b}, {c}, {d}, {e}, {f}, {g}, {h}, {i}, {j}, {k}, {l}, {m}")
        
        data={"a":a,"b":b,"c":c,"d":d,"e":e,"f":f,"g":g,"h":h,"i":i,"j":j,"k":k,"l":l,"m":m}
        update=1
        return render(request, 'user/index.html',{'title':'fetch details',"a":a,"b":b,"c":c,"d":d,"e":e,"f":f,"g":g,"h":h,"i":i,"j":j,"k":k,"l":l,"m":m,"update":update})
    except Exception as e:
        print(f"Error in fetchdetails: {e}")
        return render(request, 'user/error.html', {'error': f'Database error: {e}'})

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
    name = request.GET.get("name", "")
    print("patient name is",name)
    econtact = request.GET.get("econtact", "")
    print("patient econtact is",econtact)
    Adress = request.GET.get("Adress", "")
    print("Adress is",Adress)
    Mhistory = request.GET.get("Mhistory", "")
    print("Mhistory is",Mhistory)
    pAge = request.GET.get("pAge", "")
    pbloodgrp = request.GET.get("pbloodgrp", "")
    cdh = request.GET.get("cdh", "")
    sah = request.GET.get("sah", "")
    folowup = request.GET.get("folowup", "")
    occupation = request.GET.get("occupation", "")
    state = request.GET.get("state", "")
    
    
    import datetime

    x = datetime.datetime.now()

    print(x)

    timestamp = x
 
    
    # Use local database fallback
    data = load_local_data()
    patientids = data.get("patientids", {})
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
        # face_dataset.main(n)  # Temporarily disabled to avoid TensorFlow issues
    else:
        print("update record no new id generated")
        print("patient id is", e)
        n=e
        if name=="":
            name=data.get("a", "")
            print("blank",name)
        if econtact=="":
            econtact=data.get("b", "")
            print("blank",econtact)
        if Adress=="":
            Adress=data.get("c", "")
            print("blank",Adress)
        if Mhistory=="":
            Mhistory=data.get("d", "")
            print("blank",Mhistory)
        if pAge=="":
            pAge=data.get("f", "")
            print("blank",pAge)
        if pbloodgrp=="":
            pbloodgrp=data.get("g", "")
            print("blank",pbloodgrp)
        
        if cdh=="":
            cdh=data.get("h", "")
            print("blank",cdh)
            
        if sah=="":
            sah=data.get("i", "")
            print("blank",sah)
            
        if folowup=="":
            folowup=data.get("j", "")
            print("blank",folowup)
        if occupation=="":
            occupation=data.get("k", "")
            print("blank",occupation)
        if state=="":
            state=data.get("l", "")
            print("blank",state)
        
    n=str(n)
    print("n is ",n)
    
    # Save to local database
    try:
        print(f"Attempting to save patient data for ID: {n}")
        print(f"Patient name: {name}")
        # Update the data
        data["patientids"][n] = name
        data["patientDetails"][n] = {
            "name": name,
            "econtact": econtact,
            "Adress": Adress,
            "Mhistory": Mhistory,
            "pid": n,
            "pAge": pAge,
            "pbloodgrp": pbloodgrp,
            "cdh": cdh,
            "sah": sah,
            "folowup": folowup,
            "occupation": occupation,
            "state": state,
            "timestamp": timestamp
        }
        
        print(f"Data prepared for saving: {data}")
        
        if save_local_data(data):
            print("Patient data saved successfully")
        else:
            print("Warning: Failed to save patient data")
    except Exception as e:
        print(f"Local database error: {e}")
        return render(request, 'user/error.html', {'error': f'Failed to save patient data: {e}'})
    
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
