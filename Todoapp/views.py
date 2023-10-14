from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Task
from django.urls import reverse_lazy
# this import just helps redirect a user to a certain view 
# see if it is valid for only a class based view

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class CustomLogin(LoginView):
    template_name = 'Todoapp/login.html'
    fields = '__all__' # see to customise fields later on 
    redirect_authenticated_user = True # see the effect of this
    # user automaticaly gets redirected to page on accesing /login if already loggedin
    # setting the above to True another user can't access the loginpage..
    #.. on same browser unless the loggedin in user loggs out

    #see the effect of this method defined here
    # note if not specified it would redirect to accounts/profile by default
    def get_success_url(self):
        return reverse_lazy('tasks')
        # note the task here is the name of the url route not a context




class TodoList(LoginRequiredMixin, ListView):
    model = Task    # model class to fetch details from
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()
        
        search_input = self.request.GET.get('searchtext') or '' #the or is for None not to be displayed
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['lastsearch'] = search_input    

        return context




class TodoDetail(DetailView):
    model = Task  
    context_object_name = 'renamed_object'  # ths is to reassing default contex name
    template_name = 'Todoapp/more.html'   # this is to reassign default template name path

# note the DetailView returns a partcula item based on its pk id/int
# while the ListView returns a list of all items in the Model 
# also note the naming patters of templates class views route to ..I.e modelname_clsviewCustomName


# you can name the class as you wish ..just used this naming patterns for consistency 
class TodoCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__'  #all fields were selected but the form_valid would auto select logged in user
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form) 
    
class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']  #use a list to select particular views 
    success_url = reverse_lazy('tasks')  

class ItemDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'Todoapp/delete.html' # to ovewrite the custom template name needed
    success_url = reverse_lazy('tasks')
    # used same context_name as specified in the main page   

class Register(FormView):
    template_name = 'Todoapp/register.html'
    form_class = UserCreationForm    # see how to get other details from user on creation 
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()

        # this is just to redirect the user to specific page on succesful reg
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)


def sample(request):
    return HttpResponse('hello welcome to our app') 


#Todo: see how to use a function based view to work this out later on 
# def register(request):
#     return render(request, 'Todoapp/register.html')