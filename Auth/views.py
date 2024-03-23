from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Stream import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .middlewares import auth, guest
from django.contrib.sessions.models import Session
from .models import *
import random
# Create your views here.
@auth
def home(request):
    video = Video.objects.all()
    data = get_object_or_404(UserInfo, user=request.user)
    context = {
        'video': video,
        'profile': data,
    }
    return render(request, "authentication/video.html", context)
@guest
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        messages.success(request, "Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to StreamSync !!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to  StreamSync  \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n StreamSync "        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @  StreamSync !!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")

@guest
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

@guest
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        pass1 = request.POST['pass1']
        
        # Check if username_or_email is an email
        if '@' in username_or_email:
            # Authenticate using email
            user = authenticate(email=username_or_email, password=pass1)
        else:
            # Authenticate using username
            user = authenticate(username=username_or_email, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Successfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")

@auth
def live(request):
    return render(request, "authentication/stream.html", {'username': request.user.username})

@auth
def profile(request):
    data = get_object_or_404(UserInfo, user=request.user)
    return render(request, "authentication/profile.html", {'data': data})
@auth
def edit(request):
    data = get_object_or_404(UserInfo, user=request.user)
    if request.method == 'POST':
        user = request.user
        if 'fname' in request.POST and request.POST['fname']:
            user.first_name = request.POST['fname']
        if 'lname' in request.POST and request.POST['lname']:
            user.last_name = request.POST['lname']
        if 'username' in request.POST and request.POST['username']:
            user.username = request.POST['username']
        if 'email' in request.POST and request.POST['email']:
            user.email = request.POST['email']
        #userinfo        
        if 'profile' in request.FILES:
            profile_image = request.FILES['profile']
            data.profile = profile_image
        if 'country' in request.POST and request.POST['country']:
            data.country = request.POST['country']
        if 'address' in request.POST and request.POST['address']:
            data.address = request.POST['address']
        if 'bio' in request.POST and request.POST['bio']:
            data.bio = request.POST['bio']
        try:
            user.save()
            data.save()
        except Exception as e:
            print(request, f'An error occurred: {str(e)}')
        return redirect('profile')
    return render(request, "authentication/profile_update.html", {'data': data})

@auth
def event(request):
    event = Events.objects.all()
    return render(request, "authentication/event.html", {'username': request.user.username, "event" : event})

@auth
def newspost(request, title):
    data = get_object_or_404(News, title=title)
    news = News.objects.exclude(title=title)
    current_post_url = request.build_absolute_uri()
    return render(request, "authentication/post.html", {'data': data})

@auth
def video(request):
    return render(request, "authentication/video.html")

@auth
def player(request,title):
    data = get_object_or_404(Video, title=title)
    data.views += 1
    data.save()
    comments = Comment.objects.filter(video=data.id)
    total_comments = comments.count()
    all_videos = Video.objects.exclude(title=title)
    random_videos = random.sample(list(all_videos), min(3, len(all_videos)))
    if request.method == 'POST':
        video = data
        user = request.user
        text = request.POST['text']
        comment = Comment.objects.create(video=video, user=user, text=text)
        comment.save()

    return render(request, "authentication/player.html",{'data': data,"video": random_videos, 'comments': comments, 'total_comments': total_comments })

@auth
def upload(request):
    context = News.objects.all()
    return render(request, 'authentication/upload.html', {'context' : context})

@auth
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')