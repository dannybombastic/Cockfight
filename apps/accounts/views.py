from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import (ListView, CreateView, DeleteView,
                                    UpdateView, DetailView)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, EditProfileForm
from .models import *

def register(request):
    if request.method == 'POST':
        f = RegistroForm(request.POST)
        if f.is_valid():
            f.save()
        #creo extension in model for signals
        #    usuario = userProfile()
        #    usuario.user = f
        #    usuario.save()
            messages.success(request, 'Cuenta creada, ya puedo hacer Login')
            return redirect('/accounts/registrar/')
    else:
        f = RegistroForm()
    return render(request, 'accounts/registrar.html', {'form': f})

class Profile_views(LoginRequiredMixin, DetailView):
    model = userProfile
    template_name = 'accounts/profile.html'

class EditProfile_views(LoginRequiredMixin, UpdateView):
    model = userProfile
    form_class = EditProfileForm
    template_name = 'accounts/editProfile.html'
    #success_url = reverse_lazy('accounts:profile')

    def get_success_url(self):
          # if you are passing 'pk' from 'urls'
          # capture that 'pk' and pass it to 'reverse_lazy()' function
          id_user=self.kwargs['pk']
          return reverse_lazy('accounts:profile', kwargs={'pk': id_user})
