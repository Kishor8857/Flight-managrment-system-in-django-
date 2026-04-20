from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('history/', views.booking_history, name='history'),
    path('support/', views.support, name='support'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change-password'),
    path('manage-flights/', views.add_flight, name='add-flight'),
    path('manage-flights/edit/<int:flight_id>/', views.edit_flight, name='edit-flight'),
    path('manage-flights/delete/<int:flight_id>/', views.delete_flight, name='delete-flight'),
]
