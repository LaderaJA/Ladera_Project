from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden, JsonResponse
from .models import Design, Like, Comment, Follow, OverlayLog
from account.models import CustomUser
from django.utils.timezone import now
from .forms import CommentForm
from django.views.generic.edit import FormView
from django.views import View



class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['designs'] = Design.objects.all()[:10]  
        return context

class DesignListView(ListView):
    model = Design
    template_name = 'pages/design_list.html'  
    context_object_name = 'designs'

class DesignDetailView(DetailView):
    model = Design
    template_name = 'pages/design_detail.html'
    context_object_name = 'design'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        design = self.get_object()
        user = self.request.user
        
        if user.is_authenticated:
            context['can_edit_or_delete'] = (
                user == design.creator or user.is_staff or (user.is_moderator == True)
            )
        else:
            context['can_edit_or_delete'] = False
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object =  self.get_object()
        if form.is_valid():
            comment = form.save( commit=False )
            comment.user = request.user
            comment.design = self.object
            comment.save()
            return redirect(reverse('design-detail', kwargs = {'pk' : self.object.pk}))
        return self.get(self, request, *args, **kwargs)

    

    
class DesignCreateView(LoginRequiredMixin, CreateView):
    model = Design
    fields = ['title', 'description', 'image']
    template_name = 'pages/design_form.html'
    success_url = reverse_lazy('design-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class DesignUpdateView(LoginRequiredMixin, UpdateView):
    model = Design
    fields = ['title', 'description', 'image']
    template_name = 'pages/design_form.html'
    
    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.pk}) 

class DesignDeleteView(LoginRequiredMixin, DeleteView):
    model = Design
    template_name = 'pages/design_confirm_delete.html'
    success_url = reverse_lazy('design-list')  
    

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = "pages/comment_form.html"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.design.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "pages/confirm_comment_delete.html"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs = {'pk': self.object.design.pk})
    

# like functions

class LikeDesignView(View):
    def post(self, request, pk):
        design = get_object_or_404(Design, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, design=design)

        if not created:
            like.delete()
        
        return redirect('design-detail', pk=pk)

# follow functions

class FollowUserView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        followed_user = get_object_or_404(settings.AUTH_USER_MODEL, id=kwargs['pk'])
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
        return JsonResponse({"status": "followed"})

class OverlayLogView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        design = get_object_or_404(Design, id=kwargs['pk'])
        OverlayLog.objects.create(user=request.user, design=design, applied_at=now())
        return JsonResponse({"status": "Overlay logged successfully."})


# camera
class CameraFilterView(TemplateView):
    template_name = 'pages/camera_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['designs'] = Design.objects.all()
        return context


# User profile


