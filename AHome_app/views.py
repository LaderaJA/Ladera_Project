from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden, JsonResponse
from .models import Design, Like, Comment, Follow, OverlayLog, CustomUser
from django.utils.timezone import now
from .forms import CommentForm



class HomePageView(TemplateView):
    template_name = 'pages/home.html'

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

class DesignCreateView(CreateView):
    model = Design
    fields = ['title', 'description', 'image']
    template_name = 'pages/design_form.html'
    success_url = reverse_lazy('design-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class DesignUpdateView(UpdateView):
    model = Design
    fields = ['title', 'description', 'image']
    template_name = 'pages/design_form.html'
    
    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.pk}) 

class DesignDeleteView(DeleteView):
    model = Design
    template_name = 'pages/design_confirm_delete.html'
    success_url = reverse_lazy('design-list')  
    

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['content']
    template_name = "pages/comment_form.html"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.design.pk})

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "pages/confirm_comment_delete.html"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs = {'pk': self.object.design.pk})
    


class LikeDesignView( CreateView):
    def post(self, request, *args, **kwargs):
        design = get_object_or_404(Design, id=kwargs['pk'])
        Like.objects.get_or_create(user=request.user, design=design)
        return JsonResponse({"status": "liked"})



class FollowUserView( CreateView):
    def post(self, request, *args, **kwargs):
        followed_user = get_object_or_404(CustomUser, id=kwargs['pk'])
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
        return JsonResponse({"status": "followed"})

class OverlayLogView(CreateView):
    def post(self, request, *args, **kwargs):
        design = get_object_or_404(Design, id=kwargs['pk'])
        OverlayLog.objects.create(user=request.user, design=design, applied_at=now())
        return JsonResponse({"status": "Overlay logged successfully."})


def camera_filter_view(request):
    designs = Design.objects.all()
    return render(request, 'pages/camera_filter.html', {'designs': designs})