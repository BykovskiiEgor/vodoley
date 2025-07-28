from django.urls import path
from . import views
    
app_name = 'api'

urlpatterns = [   
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('get-password/', views.SendTPForLogIn.as_view(), name='password'),
    path('create-user/', views.RegisterUserView.as_view(), name='create user'),
    path('update-email/', views.EditUserEmail.as_view(), name='edit email'),
    path('update-phone/', views.EditUserPhone.as_view(), name='edit phone number'),
]
