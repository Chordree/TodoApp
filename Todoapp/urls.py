from django.urls import path
from . import views
from .views import TodoDetail, TodoCreate, TodoUpdate
# see the diff accesing CbVs from this two methds of import
# note the two various stlyes of import

from django.contrib.auth.views import LogoutView
# importing  a ready made view directly from django>contrib

urlpatterns = [
    path('login/',views.CustomLogin.as_view(), name='loginpage'),
    path('logout/', LogoutView.as_view(next_page = 'tasks'), name='logout'),
    path('register', views.Register.as_view(), name='registerpage'),
    path('',views.TodoList.as_view(), name='tasks'),
    path('sample', views.sample, name='example'),
    path('det/<int:pk>/', TodoDetail.as_view(), name='details'),
    path('addtask', TodoCreate.as_view(), name='additem'),
    path('edit/<int:pk>/', TodoUpdate.as_view(), name='editItem'),
    path('delete/<int:pk>/', views.ItemDelete.as_view(), name='deletetask')
]

# note detailview must be called with a int: pk
# check the effect of adding the second / in a pk path

# note for the logout if the default parameter is not set it would 
#..redirect to the django logout page 

# note path(urlroute on browser, viewname, redirectname views and template)