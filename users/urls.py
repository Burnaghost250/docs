from django.contrib import admin
from django.conf import settings
from django.urls import path

from .views  import animate_view,home_view,login_view,admin_view,delete_user,success_view,signup_view,user_dashboard_view,upload_view,logout_view,files,delete_uploads,update_settings,profile_view,privacy,message_us
from django.conf.urls.static import static


 
urlpatterns = [
    path('',animate_view,name='animate'),
    path('home/',home_view, name='home'),
    path('login/',login_view,name='login'),
    path('signup/',signup_view, name='signup'),
    path('boss/',admin_view,name='boss'),
    path('del_user/<int:user_id>/',delete_user,name='delete_user'),
    path('success/',success_view,name='success'),
    path('profile/',profile_view,name='profile'),
    path('dashboard/',user_dashboard_view,name='dashboard'),
    path('upload/',upload_view,name='upload'),
    path('logout/',logout_view,name='logout'),
    path('files/',files,name='files'),
    path('delete/<int:upload_id>/', delete_uploads, name='delete_upload'),
    path('sms/',message_us,name="sms"),
    path('settings/',update_settings,name='update_settings'),
    path('privacy/',privacy,name='privacy')
    
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)