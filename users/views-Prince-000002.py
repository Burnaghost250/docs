from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Upload,ProfilePicture
from datetime import datetime
from django.core.mail import send_mail

# Views on a single page
def animate_view(request):
    return render(request,'anime.html')
def home_view(request):
    # Home view
    return render(request, 'welcome.html')

def login_view(request):
    # Login view
    if request.user.is_authenticated:
        return redirect('dashboard') 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if  request.user.is_superuser: 
                return redirect('boss')

        return redirect('dashboard')
    
        

    return render(request, 'login.html')

def signup_view(request):
    # Signup view
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')

        if password != conf_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists")
            return render(request, 'signup.html')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        return redirect('success')

    return render(request, 'signup.html')



@login_required
def admin_view(request):
    users = User.objects.all()
    superuser = User.objects.filter(is_superuser=True).first()
    context = {
        'username':request.user.username,
        'users': users,  
        'superuser': superuser.username if superuser else "No superuser found",
    }

    return render(request, 'admin.html', context)

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_authenticated and request.user.is_superuser:
        user.delete()  
        user.save()
    return redirect('boss')   
@login_required    
def logout_view(request):
   
    logout(request)
    request.session.flush()  # Clear all session data
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        profile_pic = request.FILES.get('profile_pic')  # Ensure correct field name

        # Retrieve or create profile picture entry for the user
        profile_instance, created = ProfilePicture.objects.get_or_create(user=request.user)

        # Update profile picture field
        profile_instance.profile_pic = profile_pic  
        profile_instance.save()
        messages.success(request, 'Profile uploaded successfully!')
    else:
        messages.info(request, 'Please add a profile picture first.')

    username=request.user.username  
    context={
            'username':username,
        }
    return render(request, 'profile.html',context)

@login_required
def user_dashboard_view(request):
    
    # User dashboard view
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    profile_pics=ProfilePicture.objects.filter(user=request.user)
    context = {
        'username': request.user.username,
        'date': date,
        'profile_pics': profile_pics,
    }
    
    return render(request, 'user_home.html', context)
    




@login_required
def upload_view(request):
    # Upload view
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        file_choose = request.FILES.get('file_choose')

        upload = Upload.objects.create(user=request.user,title=title, description=description, file_choose=file_choose)
        upload.save()
        return redirect('files')
    return redirect('dashboard')

@login_required
def files(request):
    uploads = Upload.objects.filter(user=request.user)
    context={
        'username': request.user.username,
        'uploads':uploads,
    }
    return render(request, 'files.html', context)

@login_required
def delete_uploads(request, upload_id):
    # Delete upload view
    upload = get_object_or_404(Upload, id=upload_id)
    upload.delete()
    return redirect('files')

@login_required
def update_settings(request):
    # Update settings view
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        theme = request.POST.get('theme')

        if new_password and new_password == confirm_password:
            if user.check_password(old_password):
                user.set_password(new_password)
            else:
                messages.error(request, "Current password is incorrect")

        user.username = username
        user.email = email
        user.save()
        messages.success(request, "Settings updated successfully")
        return redirect('update_settings')

    return render(request, 'settings.html', {'user': request.user})

def success_view(request):
    # Success page view
    return render(request, 'success.html')


@login_required
def dashboard_view(request):
    # Protected dashboard view
    return render(request, 'dashboard.html', {'username': request.user.username})
@login_required
def message_us(request):
    if request.method=="POST":
        usname=request.POST.get('usname')
        email=request.POST.get('email')
        msg=request.POST.get('msg')

        username=request.user.username
       
        
    context={
            'username':request.user.username,
        }
    return render(request,'sms.html',context)





def privacy(request):
    return render(request,'privacy.html')