# Create your views here.
from django.shortcuts import render,redirect
# imported our models
from django.views.generic import DetailView
from django.core.paginator import Paginator
from . models import Video
from django.contrib import messages
from django.contrib.auth.models import User, auth



class VideoDetailView(DetailView):
    model = Video
    template_name = "play.html"
    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        return context

def videos(request):
    paginator= Paginator(Video.objects.all(),2)
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
            return redirect("App:enroll")
    return render(request,"register.html")

def enroll(request):
    return render(request,"enroll.html")

def verify(request):
    return render(request,"verify.html")
