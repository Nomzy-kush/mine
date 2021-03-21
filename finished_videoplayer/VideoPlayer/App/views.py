# Create your views here.
from django.shortcuts import render,redirect
# imported our models
from django.views.generic import DetailView
from django.core.paginator import Paginator
from . models import Video,UserProfile
from django.contrib import messages
from django.contrib.auth.models import User, auth
import hashlib
from . typingdna import TypingDNA

tdna = TypingDNA("apiKey","apiSecret")



class VideoDetailView(DetailView):
    model = Video
    template_name = "play.html"
    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        return context

def videos(request):
    paginator= Paginator(Video.objects.filter(user=request.user),2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request,"videos.html",context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if 'user' in request.session:
                return redirect("App:videos")
            else:
                return redirect("App:verify")
        else:
            context={"message":"Invalid login credentials"}
            return render(request,"login.html",context)
    else:
        return render(request,"login.html")

def register(request):
    if request.method=="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            context={"message":"user already exists"}
            return render(request,"register.html",context)
        else:
            request.session["reg_user"] = {
                    "username": username
                }
            user = User.objects.create(username=username,password=password, email=email)
            user.set_password(user.password)
            user.is_staff = True
            user.save()
            userprofile=UserProfile.objects.create(user=user)
            userprofile.save()
            return redirect("App:enroll")
    return render(request,"register.html")

def enroll(request):
    if request.method=="POST":
        tp = request.POST.get("tp")
        username = request.session["reg_user"]["username"]
        r = tdna.auto(tdna.hash_text(username), tp)
        if r.status_code == 200:
            print(username)
            user=UserProfile.objects.get(user=User.objects.get(username=username))
            user.typingdna_secured=True
            user.save()
            request.session["typingdna_auth"] = True
            messages.add_message(request, messages.INFO,"You have successfully registered TypingDNA 2FA", "success")
            return redirect("App:videos")
        else:
            messages.add_message(request, messages.INFO,r.json()["message"], "danger")
            return redirect("App:enroll")
    return render(request,"enroll.html")

def verify(request):
    if request.method == "POST":
        tp = request.POST.get("tp")
        username = request.user.username
        r = tdna.auto(tdna.hash_text(username), tp)
        if r.status_code == 200:
            if r.json()["result"] == 1:
                request.session["typingdna_auth"] = True
                return redirect("App:videos")
            else:
                messages.add_message(request, messages.INFO,"You failed the TypingDNA verification check, please try again", "danger")
                return redirect("App:verify")
        else:
            messages.add_message(request, messages.INFO,r.json()["message"], "danger")
            return redirect("App:verify")
    return render(request,"verify.html")
