from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Streaming import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .middlewares import auth, guest
from django.contrib.sessions.models import Session
from django.http import HttpResponse
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
    print(video)
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
def reset_password(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'User with this email does not exist.')
        return redirect('password_reset')  # Redirect to password reset page or any other page
    
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('profile')  # Redirect to profile or any other page
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password', email=email)
    return render(request, 'authentication/reset_password.html', {'email': email})

@auth
def password(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User does not exist")

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            print("success")
            return redirect('profile')  # Redirect to profile or any other page
        else:
            messages.error(request, 'Passwords do not match.')
            print("failed")
            return redirect('profile', email=email)

    return render(request, 'authentication/passwor.html', {'email': email})


@guest
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")

@auth
def live(request):
    data = get_object_or_404(UserInfo, user=request.user)
    context = {
        'username': request.user.username,
        'data': data,
    }
    return render(request, "authentication/stream.html",context)

@auth
def profile(request):
    upload_text = "upload"  # The text you want to pass
    request.session['upload_text'] = upload_text  # Store the text in session
    video = Video.objects.filter(user=request.user)
    data = get_object_or_404(UserInfo, user=request.user)
    return render(request, "authentication/profile.html", {'username': request.user.username,'upload_text': upload_text, "video": video, 'data' : data})

@auth
def video(request):
    data = get_object_or_404(UserInfo, user=request.user)
    video = Video.objects.all()
    context = {
        'video': video,
        'data': data,
    }
    return render(request, "authentication/video.html", context)
@auth
def trending(request):
    data = get_object_or_404(UserInfo, user=request.user)
    video = Video.objects.all().order_by('-views')
    context = {
        'video': video,
        'data': data,
    }
    return render(request, "authentication/trending.html", context)

@auth
def edit(request):
    data = get_object_or_404(UserInfo, user=request.user)
    profile = get_object_or_404(UserInfo, user=request.user)
    context = {
        'data': data,
        'profile': profile,
    }
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
    return render(request, "authentication/profile_update.html",context)


@auth
def event(request):
    event = Events.objects.all()
    data = get_object_or_404(UserInfo, user=request.user)
    context = {
        'event': event,
        'data': data,
    }
    return render(request, "authentication/event.html",context)

@auth
def newspost(request, title):
    articles = get_object_or_404(News, title=title)
    random_news = News.objects.exclude(title=title)
    news = random.sample(list(random_news), min(3, random_news.count()))
    data = get_object_or_404(UserInfo, user=request.user)
    context = {
        'articles':articles,
        'news': news,
        'data': data,
    }
    return render(request, "authentication/post.html", context)


@auth
def player(request,title):
    play = get_object_or_404(Video, title=title)
    play.views += 1
    play.save()
    data = get_object_or_404(UserInfo, user=request.user)
    comments = Comment.objects.filter(video=play.id)
    total_comments = comments.count()
    all_videos = Video.objects.exclude(title=title)
    random_videos = random.sample(list(all_videos), min(3, len(all_videos)))
    if request.method == 'POST':
        video = play
        user = request.user
        text = request.POST['text']
        comment = Comment.objects.create(video=video, user=user, text=text)
        comment.save()

    return render(request, "authentication/player.html",{'data': data,"video": random_videos,'play' : play, 'comments': comments, 'total_comments': total_comments })


@auth
def upload(request):
    data = get_object_or_404(UserInfo, user=request.user)
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        video = request.FILES.get('video')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        video_obj = Video.objects.create(
            user=user,
            title=title,
            video=video,
            description=description,
            image=image,
        )
        return redirect('profile')
    else:
        return render(request,'authentication/upload.html',{'data' :data})

@auth
def articles(request):
    context = News.objects.all()
    data = get_object_or_404(UserInfo, user=request.user)
    content = {
        'context': context,
        'profile': data,
    }
    return render(request, 'authentication/Articles.html', content)


@auth
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')