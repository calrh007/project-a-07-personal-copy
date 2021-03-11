from django.urls import include, path

from . import views

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('allauth.urls')),
    path('login/', TemplateView.as_view(template_name="workout_app/login.html")),
    path('logout/', LogoutView.as_view()),
]