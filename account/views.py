from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import CustomUser

class RegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your account has been created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating your account. Please check the details and try again.")
        return super().form_invalid(form)



class ProfileView(DetailView,LoginRequiredMixin):
    model = CustomUser
    template_name = 'account/profile.html' 
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
    
class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'account/profile_confirm_delete.html'
    success_url = reverse_lazy('home')  

    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'account/profile_edit.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user  

    def get_success_url(self):
        return reverse_lazy('profile')