from django.shortcuts import render
from .models import Tree, PlantingArea, PlantingPlan
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'plantapp/home.html')

@login_required
def tree_list(request):
    trees = Tree.objects.all()
    return render(request, 'plantapp/tree_list.html', {'trees': trees})

@login_required
def planting_area_list(request):
    areas = PlantingArea.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_area_list.html', {'areas': areas})

@login_required
def planting_plan_list(request):
    plans = PlantingPlan.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_plan_list.html', {'plans': plans})
