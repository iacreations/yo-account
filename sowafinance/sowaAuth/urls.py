from django.urls import path
from . import views

# app name
app_name='sowaAuth'
urlpatterns = [    
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('otp/', views.verify_otp, name='otp'),
]
