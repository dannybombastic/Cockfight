from django.urls import path, include
from .views import register, EditProfile_views, Profile_views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    #se agrega porque toma la url por defecto
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path('', include('django.contrib.auth.urls')),
    path('registrar/', register, name='registrar'),
    path('Profile/<int:pk>/', Profile_views.as_view(), name='profile'),
    path('EditProfile/<int:pk>/', EditProfile_views.as_view(), name='EditProfile'),
]
