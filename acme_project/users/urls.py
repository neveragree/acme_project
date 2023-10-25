from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('new_user/', views.MyUserCreateView.as_view(), name='new_user'),
]
