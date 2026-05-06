from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse
from .forms import CustomUserCreationForm, TaskForm, MessageForm
from .models import Project, Task, Message
from .mixins import ProjectRoleRequiredMixin

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/dashboard.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(assignments__user=self.request.user)

class ProjectDetailView(LoginRequiredMixin, ProjectRoleRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        tasks = project.tasks.all()
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='completado').count()
        
        context['total_tasks'] = total_tasks
        context['completed_tasks'] = completed_tasks
        context['message_form'] = MessageForm()
        context['messages'] = project.messages.all().order_by('-timestamp')
        return context

class MessageCreateView(LoginRequiredMixin, ProjectRoleRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        form.instance.sender = self.request.user
        return super().form_valid(form)
        
    def form_invalid(self, form):
        return redirect('project_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs['pk']})

class TaskCreateView(LoginRequiredMixin, ProjectRoleRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        kwargs['project'] = project
        return kwargs

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs['pk']})

class TaskUpdateView(LoginRequiredMixin, ProjectRoleRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'
    pk_url_kwarg = 'task_pk'

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.object.project
        return kwargs

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})
