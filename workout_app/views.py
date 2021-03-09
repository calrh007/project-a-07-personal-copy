from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'workout_app/index.html', context)