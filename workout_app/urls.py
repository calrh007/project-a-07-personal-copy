from django.urls import include, path

from . import views

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import AddWorkoutView
from .views import WorkoutListView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('login/', TemplateView.as_view(template_name="workout_app/login.html")),
    path('logout/', LogoutView.as_view()),
    path('add_workout/', AddWorkoutView.as_view(), name='add_workout'),
    path('add_workout/workout_list', WorkoutListView.as_view(), name='workout_list'),
]