from django.urls import include, path

from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
# from .views import AddWorkoutView
# from .views import WorkoutListView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('login/', TemplateView.as_view(template_name="workout_app/login.html"), name='login'),
    path('logout/', LogoutView.as_view()),
    # path('add_workout/', AddWorkoutView.as_view(), name='add_workout'),
    # path('add_workout/workout_list', WorkoutListView.as_view(), name='workout_list'),
    path('add_workout_type/', views.newWorkoutType, name='add_workout_type'),
    path('add_workout_linked/', views.newWorkoutLinked, name='add_workout_linked'),
    path('add_workout_type_count/', views.newWorkoutTypeCount, name='add_workout_type_count'),
    path('workout_linked_list/', views.workoutLinkedListView, name='workout_linked_list'),
    path('workout_summary/', views.workoutSummary, name='workout_summary'),
    path('achievements/', views.achievementsView, name='achievements'),
    path('weather/', views.weather, name='weather'),
    # path('workout_weather/', views.workout_weather, name='workout_weather'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)